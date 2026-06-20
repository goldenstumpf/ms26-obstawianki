import os
import requests
import logging

from core.db import get_supabase

logger = logging.getLogger(__name__)

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

TIMEOUT = 15


# -----------------------------
# FETCH
# -----------------------------

def fetch_matches(competition_id: int = 2000) -> list[dict]:
    """
    Fetch matches from football-data API.
    Returns normalized list sorted by utcDate.
    """

    if not API_KEY:
        raise RuntimeError("FOOTBALL_API_KEY is missing")

    url = f"{BASE_URL}/competitions/{competition_id}/matches"

    headers = {
        "X-Auth-Token": API_KEY
    }

    logger.info(f"Fetching matches for competition={competition_id}")

    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()

    data = response.json()
    matches = data.get("matches", [])

    # sort for deterministic ordering
    matches.sort(key=lambda m: m.get("utcDate", ""))

    # add stable match numbering
    for i, match in enumerate(matches, start=1):
        match["matchNumber"] = i

    logger.info(f"Fetched {len(matches)} matches")

    return matches


# -----------------------------
# TRANSFORM
# -----------------------------

def transform_match(match: dict) -> dict:
    """
    Normalize API match → Supabase row.
    """

    score = match.get("score", {})
    ft = score.get("fullTime", {}) or {}
    et = score.get("extraTime", {}) or {}
    pen = score.get("penalties", {}) or {}

    home = match.get("homeTeam", {}) or {}
    away = match.get("awayTeam", {}) or {}

    return {
        "match_id": str(match["id"]),
        "match_number": match.get("matchNumber"),

        "utc_date": match.get("utcDate"),

        "home_team": home.get("name"),
        "away_team": away.get("name"),

        "home_code": home.get("tla"),
        "away_code": away.get("tla"),

        "status": match.get("status"),

        "stage": match.get("stage"),
        "group_name": match.get("group"),

        "duration": score.get("duration"),

        # full time
        "flt_home": ft.get("home"),
        "flt_away": ft.get("away"),

        # extra time
        "ext_home": et.get("home"),
        "ext_away": et.get("away"),

        # penalties
        "pens_home": pen.get("home"),
        "pens_away": pen.get("away"),

        "home_crest": home.get("crest"),
        "away_crest": away.get("crest"),
    }


# -----------------------------
# DB WRITE
# -----------------------------

def save_matches_to_supabase(matches: list[dict]) -> None:
    """
    Upsert matches into Supabase.
    """

    if not matches:
        logger.warning("No matches to save")
        return

    rows = [transform_match(m) for m in matches]

    logger.info(f"Upserting {len(rows)} matches to Supabase")

    get_supabase().table("matches") \
        .upsert(rows, on_conflict="match_id") \
        .execute()

    logger.info("Matches upsert completed")


# -----------------------------
# PIPELINE
# -----------------------------

def run_fetch_matches(competition_id: int = 2000) -> list[dict]:
    """
    Full ingestion pipeline:
    1. fetch
    2. transform
    3. persist
    """

    matches = fetch_matches(competition_id)
    save_matches_to_supabase(matches)

    return matches


# -----------------------------
# CLI
# -----------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    matches = run_fetch_matches()
    print(f"Zapisano {len(matches)} meczów do Supabase")