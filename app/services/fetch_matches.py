import os
import requests
from app.core.db import supabase
from datetime import datetime, timezone, timedelta

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://api.football-data.org/v4"

def resolve_monitoring(status, utc_date):

    if status in ["FINISHED", "CANCELLED", "POSTPONED"]:
        return False

    kickoff = datetime.fromisoformat(
        utc_date.replace("Z", "+00:00")
    )

    now = datetime.now(timezone.utc)

    return kickoff - now < timedelta(hours=1)

def fetch_matches(competition_id=2000):
    """
    Pobiera mecze dla danej ligi (domyślnie dla Mistrzostw Świata) korzystając z football-data.org.
    """

    url = f"{BASE_URL}/competitions/{competition_id}/matches"

    headers = {
        "X-Auth-Token": API_KEY
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status

    data = response.json()

    matches = data.get("matches", [])

    matches.sort(key=lambda m: m["utcDate"])

    for i, match in enumerate(matches, start=1):
        match["matchNumber"] = i

    return matches


def save_matches_to_supabase(matches):

    rows = []

    for match in matches:

        score = match.get("score", {})
        ft = score.get("fullTime", {})
        et = score.get("extraTime", {})
        pen = score.get("penalties", {})

        rows.append({
            "match_id": str(match["id"]),
            "match_number": match["matchNumber"],
            "utc_date": match["utcDate"],
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"],
            "home_code": match["homeTeam"]["tla"],
            "away_code": match["awayTeam"]["tla"],

            "status": match["status"],

            "stage": match.get("stage"),
            "group_name": match.get("group"),

            "duration": match.get("score", {}).get("duration"),

            "flt_home": ft.get("home"),
            "flt_away": ft.get("away"),

            "ext_home": et.get("home"),
            "ext_away": et.get("away"),

            "pens_home": pen.get("home"),
            "pens_away": pen.get("away"),

            "home_crest": match["homeTeam"].get("crest"),
            "away_crest": match["awayTeam"].get("crest"),

            "needs_monitoring": resolve_monitoring(
                match["status"],
                match["utcDate"]
            )
        })

    supabase.table("matches").upsert(
        rows,
        on_conflict="match_id"
    ).execute()

if __name__ == "__main__":
    matches = fetch_matches()
    save_matches_to_supabase(matches)
    print(f"Zapisano {len(matches)} meczów do Supabase")