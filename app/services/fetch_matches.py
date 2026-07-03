import logging
import os

import requests

from app.data.match_ingest import upsert_matches

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

    for match in matches:
        if match.get("score", {}).get("duration") == "PENALTY_SHOOTOUT":
            print(match)

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
    """Normalize football-data API match → Supabase row.

    Important:
    - football-data's `score.fullTime` may include penalties for matches decided
      in a shootout.
    - For our game, we persist:
      - flt_* as the final score *before* penalties (after ET if played)
      - pens_* as the penalty shootout score (when available)
    """

    score = match.get("score", {}) or {}

    # football-data uses home/away keys in the score objects
    ft = score.get("fullTime", {}) or {}
    rg = score.get("regularTime", {}) or {}
    et = score.get("extraTime", {}) or {}
    pen = score.get("penalties", {}) or {}

    ft_home = ft.get("home")
    ft_away = ft.get("away")

    rg_home = rg.get("home")
    rg_away = rg.get("away")

    et_home = et.get("home")
    et_away = et.get("away")

    pen_home = pen.get("home")
    pen_away = pen.get("away")

    duration = score.get("duration")

    # Derive the final score *before* penalties.
    # If a shootout happened, football-data may report fullTime as (pre-pen + pens).
    if (
        duration == "REGULAR"
        and rg_home is not None
        and rg_away is not None
    ):
        flt_home = rg_home
        flt_away = rg_away

    elif (
        duration in ["EXTRA_TIME", "PENALTY_SHOOTOUT"]
        and rg_home is not None
        and rg_away is not None
        and et_home is not None
        and et_away is not None
    ):
        flt_home = rg_home + et_home
        flt_away = rg_away + et_away
    
    else:
        flt_home = ft_home
        flt_away = ft_away


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

        "duration": duration,
        "minute": score.get("minute"),

        # final score before penalties (after ET if played)
        "flt_home": flt_home,
        "flt_away": flt_away,

        # extra time (as provided by API; kept for possible future analysis)
        "ext_home": et_home,
        "ext_away": et_away,

        # penalties
        "pens_home": pen_home,
        "pens_away": pen_away,

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

    upsert_matches(rows)

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