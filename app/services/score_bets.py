from datetime import datetime, timezone
from decimal import Decimal
import logging

from core.db import get_supabase

logger = logging.getLogger(__name__)

LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT"
}


# -----------------------------
# MATCH HELPERS
# -----------------------------

def match_has_result(match: dict) -> bool:
    """
    Determines whether match has final (regular time) result.
    For now only considers FT (flt_home / flt_away).
    """
    return (
        match.get("flt_home") is not None
        and match.get("flt_away") is not None
    )


def resolve_bet_status(match_status: str) -> str:
    """Maps match status to bet status."""
    if match_status in LIVE_STATUSES:
        return "live"
    if match_status == "FINISHED":
        return "closed"
    return "pending"


# -----------------------------
# SCORING ENGINE
# -----------------------------

def calculate_points(bet: dict, match: dict) -> Decimal | None:
    """
    Calculates betting points:
    - 4 pts: exact score
    - 2 pts: correct goal difference
    - 1 pt: correct winner
    - +0.5 bonus: near miss (difference of 1 total goal deviation)

    Returns Decimal or None if match is not scorable.
    """

    mh = match.get("flt_home")
    ma = match.get("flt_away")

    if mh is None or ma is None:
        return None

    bh = bet.get("home")
    ba = bet.get("away")

    # exact score
    if bh == mh and ba == ma:
        points = Decimal("4")

    # correct goal difference
    elif (bh - ba) == (mh - ma):
        points = Decimal("2")

    # correct winner
    elif (bh > ba) - (bh < ba) == (mh > ma) - (mh < ma):
        points = Decimal("1")

    # no match
    else:
        points = Decimal("0")

    # bonus: near miss (total deviation = 1 goal)
    if abs(mh - bh) + abs(ma - ba) == 1:
        points += Decimal("0.5")

    return points


# -----------------------------
# DATA ACCESS
# -----------------------------

def fetch_active_bets() -> list[dict]:
    """Fetch all non-closed bets."""
    res = get_supabase().table("bets") \
        .select("*") \
        .neq("status", "closed") \
        .execute()

    return res.data or []


def fetch_matches_map(match_ids: list[str]) -> dict[str, dict]:
    """
    Batch fetch matches to avoid N+1 queries.
    Returns dict: match_id -> match
    """
    if not match_ids:
        return {}

    res = get_supabase().table("matches") \
        .select("*") \
        .in_("match_id", match_ids) \
        .execute()

    return {m["match_id"]: m for m in (res.data or [])}


# -----------------------------
# CORE UPDATE
# -----------------------------

def update_bet(bet: dict, match: dict) -> dict:
    """
    Updates single bet based on match state.

    Responsibilities:
    - resolve status
    - calculate points (if applicable)
    - update DB only if something changed
    - return lightweight change summary
    """

    new_status = resolve_bet_status(match["status"])

    old_points = bet.get("points")
    points = old_points

    scorable = match_has_result(match)

    if scorable:
        points = calculate_points(bet, match)

    # detect changes
    score_updated = old_points is not None and old_points != points
    newly_scored = old_points is None and points is not None

    # skip unnecessary writes
    if (
        new_status == bet.get("status")
        and points == old_points
        and match.get("flt_home") == bet.get("flt_home")
        and match.get("flt_away") == bet.get("flt_away")
    ):
        return {
            "checked": True,
            "scorable": scorable,
            "score_updated": False,
            "newly_scored": False,
            "status": new_status,
            "skipped": True
        }

    get_supabase().table("bets").update({
        "status": new_status,
        "points": float(points) if points is not None else None,
        "flt_home": match.get("flt_home"),
        "flt_away": match.get("flt_away"),
        "ext_home": match.get("ext_home"),
        "ext_away": match.get("ext_away"),
        "pen_home": match.get("pen_home"),
        "pen_away": match.get("pen_away"),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }).eq("username", bet["username"]) \
      .eq("match_id", bet["match_id"]) \
      .execute()

    return {
        "checked": True,
        "scorable": scorable,
        "score_updated": score_updated,
        "newly_scored": newly_scored,
        "status": new_status,
        "skipped": False
    }


# -----------------------------
# MAIN RUNNER
# -----------------------------

def run_scoring() -> dict:
    """
    Main scoring pipeline:

    1. Fetch active bets
    2. Batch fetch matches (avoid N+1)
    3. Update each bet if needed
    4. Collect stats
    """

    bets = fetch_active_bets()

    match_ids = list({b["match_id"] for b in bets})
    matches_map = fetch_matches_map(match_ids)

    checked = 0
    scorable = 0
    score_updated = 0
    newly_scored = 0

    for bet in bets:
        match = matches_map.get(bet["match_id"])

        if not match:
            logger.warning(f"Missing match for bet: {bet['match_id']}")
            continue

        result = update_bet(bet, match)

        checked += 1

        if result["scorable"]:
            scorable += 1

        if result["score_updated"]:
            score_updated += 1

        if result["newly_scored"]:
            newly_scored += 1

        logger.info(
            f"Bet {bet['username']} match={bet['match_id']} "
            f"status={result['status']} "
            f"scored={result['scorable']} "
            f"updated={result['score_updated']}"
        )

    return {
        "checked": checked,
        "scorable": scorable,
        "score_updated": score_updated,
        "newly_scored": newly_scored
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    result = run_scoring()
    print("Scoring done:", result)