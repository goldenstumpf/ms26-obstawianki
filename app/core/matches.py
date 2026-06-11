from datetime import datetime, timedelta, timezone
from utils.json_io import load_json

def get_matches():
    return load_json("app/data/matches.json")


def get_bettable_matches(matches, hours=48):
    now = datetime.now(timezone.utc)
    limit = now + timedelta(hours=hours)

    filtered = []

    for m in matches:
        home = m.get("homeTeam")
        away = m.get("awayTeam")

        if not home or not away:
            continue
        if not home.get("name") or not away.get("name"):
            continue

        utc_date = m.get("utcDate")
        if not utc_date:
            continue

        match_time = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))

        if now <= match_time <= limit:
            filtered.append(m)

    return filtered

def parse_kickoff(utc_string: str):
    return datetime.fromisoformat(utc_string.replace("Z", "+00:00"))