import os
import logging
from decimal import Decimal

from app.data.bets import list_active_bets
from app.data.scoring import fetch_matches_map as fetch_matches_map_dal
from app.data.scoring import update_bet_row

logging.basicConfig(level=logging.INFO)
if os.getenv("APP_DEBUG") == "1":
    logging.getLogger().setLevel(logging.DEBUG)

# additionally silence chatty libs by default
for name in ["httpcore", "hpack", "httpx"]:
    logging.getLogger(name).setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# -----------------------------
# MATCH STATE HELPERS
# -----------------------------

LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT",
    "LIVE",
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

KNOCKOUT_STAGES = {
    "FINAL",
    "THIRD_PLACE",
    "SEMI_FINALS",
    "QUARTER_FINALS",
    "LAST_16",
    "LAST_32",
    "LAST_64",
    "ROUND_4",
}


def _sign(x: int) -> int:
    return (x > 0) - (x < 0)


def _is_knockout(match: dict) -> bool:
    return match.get("stage") in KNOCKOUT_STAGES


def _parse_penalty_dip(dip: str | None) -> str | None:
    """Return team code after 'karne:' if dip is penalty-type."""
    if not dip:
        return None
    d = dip.strip()
    if not d.lower().startswith("karne"):
        return None
    # Accept: "karne: GER" or "karne GER"
    d = d.replace("karne", "", 1).strip()
    if d.startswith(":"):
        d = d[1:].strip()
    return d or None


def _penalty_winner_code(match: dict) -> str | None:
    """Resolve winner code using penalties when available.

    Falls back to pre-penalties final score (flt) if penalty scores are missing.
    """
    ph = match.get("pens_home")
    pa = match.get("pens_away")
    if ph is not None and pa is not None:
        if ph > pa:
            return match.get("home_code")
        if pa > ph:
            return match.get("away_code")
        return None

    # fallback
    mh = match.get("flt_home")
    ma = match.get("flt_away")
    if mh is None or ma is None:
        return None
    if mh > ma:
        return match.get("home_code")
    if ma > mh:
        return match.get("away_code")
    return None


def calculate_points(bet: dict, match: dict) -> Decimal | None:
    """Calculate points for a single bet.

    Base points:
    - 4 pts: dokładny wynik (exact score)
    - 2 pts: różnica bramek (goal difference)
    - 1 pt: rezultat (winner/draw) — draw is only a valid 'rezultat' in GROUP_STAGE
    - +0.5 bonus: pudło o jednego gola (sum of abs deltas == 1)

    DIP (knockout only):
    - Duration DIP (+1) if dip is '90' or '120' and matches duration, but only if base >= 1.
    - Penalty DIP (+1) if dip is 'karne: XXX' and predicted winner in penalties is correct,
      even if base points are 0.

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

    stage = match.get("stage")
    duration = match.get("duration")
    dip = bet.get("dip")

    is_knockout = _is_knockout(match)

    base = Decimal("0")

    # exact score
    if bh == mh and ba == ma:
        base = Decimal("4")

    # correct goal difference
    elif (bh - ba) == (mh - ma):
        base = Decimal("2")

    else:
        # rezultat
        if not is_knockout:
            # group stage: allow draw rezultat based purely on full-time score
            bet_sign = _sign(bh - ba)
            match_sign = _sign(mh - ma)
            if bet_sign == match_sign:
                base = Decimal("1")
        else:
            # knockout: a winner must exist; resolve winner for bet & match
            # - bet winner is from score sign if non-draw, otherwise from penalty DIP ('karne: XXX')
            # - match winner is from penalties when present, fallback to full-time (pre-penalties) score
            match_winner = _penalty_winner_code(match)

            bet_winner: str | None
            bet_sign = _sign(bh - ba)
            if bet_sign > 0:
                bet_winner = match.get("home_code")
            elif bet_sign < 0:
                bet_winner = match.get("away_code")
            else:
                bet_winner = _parse_penalty_dip(dip)

            if match_winner and bet_winner and str(match_winner).upper() == str(bet_winner).upper():
                base = Decimal("1")

    points = base

    # bonus: near miss (applies always when match has score)
    if abs(mh - bh) + abs(ma - ba) == 1:
        points += Decimal("0.5")

    # DIP handling (knockout only)
    if is_knockout:
        penalty_pick = _parse_penalty_dip(dip)
        if penalty_pick:
            # Penalty DIP bonus only applies when the match was decided on penalties.
            if match.get("duration") == "PENALTY_SHOOTOUT":
                winner = _penalty_winner_code(match)
                if winner and penalty_pick.upper() == str(winner).upper():
                    points += Decimal("1")
        else:
            # duration-type DIP: '90' or '120'
            if base >= 1 and dip in {"90", "120"}:
                if (dip == "90" and duration == "REGULAR") or (
                    dip == "120" and duration == "EXTRA_TIME"
                ):
                    points += Decimal("1")

    return points


# -----------------------------
# DATA ACCESS
# -----------------------------

def fetch_active_bets() -> list[dict]:
    """Fetch all bets that are not closed."""

    return list_active_bets()


def fetch_matches_map(match_ids: list[str]) -> dict[str, dict]:
    """Batch fetch matches and return map: match_id → match."""

    return fetch_matches_map_dal(match_ids)


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
    update_bet_row(
        bet["username"],
        bet["match_id"],
        status=new_status,
        points=float(new_points) if new_points is not None else None,
    )
    
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