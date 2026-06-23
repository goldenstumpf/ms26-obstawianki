from datetime import datetime, timezone
from decimal import Decimal
import logging

from app.core.db import get_supabase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -----------------------------
# MATCH STATE HELPERS
# -----------------------------

LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT",
}


def match_has_result(match: dict) -> bool:
    """
    Returns True if match has final score (FT).
    Only full-time score is considered scorable.
    """
    return (
        match.get("flt_home") is not None
        and match.get("flt_away") is not None
    )


def resolve_bet_status(match_status: str) -> str:
    """
    Maps match status → bet status.
    """
    if match_status in LIVE_STATUSES:
        return "live"
    if match_status == "FINISHED":
        return "closed"
    return "pending"


# -----------------------------
# SCORING LOGIC
# -----------------------------

def calculate_points(bet: dict, match: dict) -> Decimal | None:
    """
    Scoring rules:
    - 4 pts: exact score
    - 2 pts: correct goal difference
    - 1 pt: correct winner
    - +0.5 bonus: near miss (total deviation = 1 goal)

    Returns None if match is not scorable.
    """

    mh = match.get("flt_home")
    ma = match.get("flt_away")

    bh = bet.get("home_bet")
    ba = bet.get("away_bet")

    if mh is None or ma is None:
        return None
    if bh is None or ba is None:
        return None

    # exact score
    if bh == mh and ba == ma:
        points = Decimal("4")

    # correct goal difference
    elif (bh - ba) == (mh - ma):
        points = Decimal("2")

    # correct winner
    elif (bh > ba) - (bh < ba) == (mh > ma) - (mh < ma):
        points = Decimal("1")

    else:
        points = Decimal("0")

    # bonus: near miss
    if abs(mh - bh) + abs(ma - ba) == 1:
        points += Decimal("0.5")

    return points


# -----------------------------
# DATA ACCESS
# -----------------------------

def fetch_active_bets() -> list[dict]:
    """
    Fetch all bets that are not closed.
    """
    res = (
        get_supabase()
        .table("bets")
        .select("*")
        .neq("status", "closed")
        .execute()
    )

    return res.data or []


def fetch_matches_map(match_ids: list[str]) -> dict[str, dict]:
    """
    Batch fetch matches and return map:
    match_id → match
    """
    if not match_ids:
        return {}

    res = (
        get_supabase()
        .table("matches")
        .select("*")
        .in_("match_id", match_ids)
        .execute()
    )

    return {m["match_id"]: m for m in (res.data or [])}


# -----------------------------
# UPDATE SINGLE BET
# -----------------------------

def update_bet(bet: dict, match: dict) -> dict:
    """
    Updates a single bet based on match state.

    Responsibilities:
    - resolve bet status
    - calculate points (if match is scorable)
    - update DB only if needed
    """

    new_status = resolve_bet_status(match["status"])

    old_points = bet.get("points")
    new_points = old_points

    # calculate points only when match has result
    if match_has_result(match):
        new_points = calculate_points(bet, match)

    #logger.info(
    #    f"user={bet['username']} match={bet['match_id']} "
    #    f"\n\tbet={bet['home_bet']}:{bet['away_bet']} "
    #    f"\n\tscore={match.get('flt_home')}:{match.get('flt_away')} "
    #    f"\n\tstatus={bet.get('status')}->{new_status} "
    #    f"\n\tpoints={old_points}->{new_points}"
    #)

    # skip DB write if nothing changed
    if new_status == bet.get("status") and new_points == old_points:
        return {
            "checked": True,
            "scorable": match_has_result(match),
            "score_updated": False,
            "newly_scored": False,
            "status": new_status,
            "skipped": True,
        }

    # update DB
    get_supabase().table("bets").update({
        "status": new_status,
        "points": float(new_points) if new_points is not None else None,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }).eq("username", bet["username"]) \
      .eq("match_id", bet["match_id"]) \
      .execute()
    
    #logger.info(
    #    f"UPDATE user={bet['username']} match={bet['match_id']} "
    #    f"\n\tbet={bet['home_bet']}:{bet['away_bet']}"
    #    f"\n\tscore={match.get('flt_home')}:{match.get('flt_away')} "
    #    f"\n\tstatus={bet.get('status')}->{new_status} "
    #    f"\n\tpoints={old_points}->{new_points}"
    #)

    return {
        "checked": True,
        "scorable": match_has_result(match),
        "score_updated": old_points is not None and old_points != new_points,
        "newly_scored": old_points is None and new_points is not None,
        "status": new_status,
        "skipped": False,
    }


# -----------------------------
# MAIN SCORING PIPELINE
# -----------------------------

def run_scoring() -> dict:
    """
    Full scoring pipeline:

    1. Fetch all active bets
    2. Batch fetch related matches
    3. Update bets if needed    
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

    return {
        "checked": checked,
        "scorable": scorable,
        "score_updated": score_updated,
        "newly_scored": newly_scored,
    }


# -----------------------------
# ENTRYPOINT
# -----------------------------

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)

    result = run_scoring()
    print("Scoring done:", result)