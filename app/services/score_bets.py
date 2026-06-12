from datetime import datetime, timezone
from app.core.db import supabase

LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT"
}

def match_has_result(match):
    return (
        match.get("flt_home") is not None and
        match.get("flt_away") is not None
    )

def resolve_bet_status(match_status):
    if match_status in LIVE_STATUSES:
        return "live"
    if match_status == "FINISHED":
        return "closed"
    return "pending"

def calculate_points(bet, match):
    mh = match.get("flt_home")
    ma = match.get("flt_away")

    if mh is None or ma is None:
        return None

    bh = bet.get("home")
    ba = bet.get("away")

    # 1. exact score
    if bh == mh and ba == ma:
        points = 4

    # 2. correct goal difference
    elif bh - ba == mh - ma:
        points = 2

    # 3. correct winner
    elif (bh > ba) - (bh < ba) == (mh > ma) - (mh < ma):
        points = 1

    # 4. no points
    else:
        points = 0

    if abs(mh - bh) + abs(ma - ba) == 1:
        points += 0.5

    return points

def fetch_active_bets():
    res = supabase.table("bets") \
        .select("*") \
        .neq("status", "closed") \
        .execute()

    return res.data or []

def update_bet(bet, match):
    new_status = resolve_bet_status(match["status"])

    old_points = bet.get("points")

    points = old_points

    if match_has_result(match):
        points = calculate_points(bet, match)

    changed_score = old_points is not None and old_points != points

    supabase.table("bets").update({
        "status": new_status,
        "points": points,
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
        "scorable": match_has_result(match),
        "score_updated": changed_score,
        "newly_scored": old_points is None and points is not None,
        "status": new_status
    }

def run_scoring():
    bets = fetch_active_bets()

    checked = 0
    scorable = 0
    score_updated = 0
    newly_scored = 0

    for bet in bets:
        match = supabase.table("matches") \
            .select("*") \
            .eq("match_id", bet["match_id"]) \
            .single() \
            .execute().data

        if not match:
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
        "newly_scored": newly_scored
    }


if __name__ == "__main__":
    result = run_scoring()
    print("Scoring done:", result)