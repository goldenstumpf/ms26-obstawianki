from datetime import datetime, timezone
from core.db import supabase

def get_all_bets():
    res = supabase.table("bets").select("*").execute()
    data = res.data or []

    grouped = {}

    for row in data:
        user = row["username"]
        match_id = str(row["match_id"])

        grouped.setdefault(user, {})[match_id] = {
            "home": row["home"],
            "away": row["away"]
        }

    return grouped

def get_user_bets_report(username: str):
    res = (
        supabase.table("bets")
        .select("*")
        .eq("username", username)
        .execute()
    )

    return res.data


def get_user_bets(username: str):
    res = (
        supabase.table("bets")
        .select("*")
        .eq("username", username)
        .execute()
    )

    data = res.data or []

    bets = {}

    for row in data:
        match_id = str(row["match_id"])
        bets[match_id] = {
            "home": row["home"],
            "away": row["away"]
        }

    return bets

def save_user_bets(username: str, bets: dict, matches: list):
    now = datetime.now(timezone.utc)

    rows = []
    saved = 0

    for match in matches:
        match_id = str(match["match_id"])

        if match_id not in bets:
            continue

        bet = bets[match_id]

        home = bet.get("home")
        away = bet.get("away")

        # NIE zapisujemy pustych typów
        if home is None or away is None:
            continue

        rows.append({
            "username": username,
            "match_id": match_id,
            "home_team": match["home_team"],
            "away_team": match["away_team"],
            "home": home,
            "away": away,
            "updated_at": now.isoformat()
        })

        saved += 1

    if rows:
        supabase.table("bets").upsert(
            rows,
            on_conflict="username,match_id"
        ).execute()

    return saved