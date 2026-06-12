from datetime import datetime, timedelta, timezone
from utils.json_io import load_json
from core.db import supabase

def get_matches():

    res = (
        supabase
        .table("matches")
        .select("*")
        .order("utc_date")
        .execute()
    )

    return res.data


def get_bettable_matches(matches, hours=72):
    now = datetime.now(timezone.utc)
    limit = now + timedelta(hours=hours)

    filtered = []

    for m in matches:
        home = m.get("home_team")
        away = m.get("away_team")

        if not home or not away:
            continue

        utc_date = m.get("utc_date")

        if not utc_date:
            continue

        match_time = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))

        if now <= match_time <= limit:
            filtered.append(m)

    return filtered

def parse_kickoff(utc_string: str):
    return datetime.fromisoformat(utc_string.replace("Z", "+00:00"))