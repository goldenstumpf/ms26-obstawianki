from datetime import datetime, timezone
from core.db import supabase
from typing import TypedDict


# =========================
# MODELS (minimal contracts)
# =========================


class BetInput(TypedDict):
    home: int | None
    away: int | None

class MatchSnapshot(TypedDict):
    match_id: str
    match_number: int
    stage: str
    group_name: str

    home_team: str
    away_team: str

    home_code: str
    away_code: str

    home_crest: str
    away_crest: str

    utc_date: str

class BetRecord(TypedDict):
    username: str
    match_id: str

    home: int | None
    away: int | None

    status: str
    points: float | None

    updated_at: str

    # snapshot meczu
    group_name: str
    home_crest: str
    away_crest: str
    home_code: str
    away_code: str
    utc_date: str

# =========================
# READ
# =========================

def get_bets(username: str | list[str] | None = None) -> list[BetRecord]:
    """
    Fetch bets.

    Args:
        username:
            - None -> all users
            - str -> single user
            - list[str] -> multiple users

    Returns:
        list[BetRecord]
    """

    query = supabase.table("bets").select("*")

    if isinstance(username, str):
        query = query.eq("username", username)

    elif isinstance(username, list):
        query = query.in_("username", username)

    res = query.execute()
    return res.data or []

# =========================
# WRITE
# =========================

def _bet_changed(existing: dict, new: dict) -> bool:
    return (
        existing.get("home") != new.get("home")
        or existing.get("away") != new.get("away")
    )

def save_bets(
    username: str,
    bets: dict[str, BetInput],
    matches: list[MatchSnapshot],
) -> dict:
    """
    Saves bets and detects real changes (diff-based upserts).
    """

    now = datetime.now(timezone.utc).isoformat()

    # 1. GET EXISTING BETS (ONLY USER)
    existing_res = (
        supabase.table("bets")
        .select("match_id, home, away")
        .eq("username", username)
        .execute()
    )

    existing_map = {
        str(r["match_id"]): r
        for r in (existing_res.data or [])
    }

    match_map = {str(m["match_id"]): m for m in matches}

    rows = []
    skipped = 0
    changed = 0

    # 2. BUILD UPSERT LIST ONLY FOR CHANGED BETS
    for match_id, bet in bets.items():
        match = match_map.get(match_id)
        if not match:
            skipped += 1
            continue

        if bet.get("home") is None or bet.get("away") is None:
            skipped += 1
            continue

        existing = existing_map.get(match_id)

        new_bet = {
            "home": bet["home"],
            "away": bet["away"],
        }

        # 3. DIFF CHECK
        if existing and not _bet_changed(existing, new_bet):
            continue  # no real change

        changed += 1

        rows.append({
            "username": username,
            "match_id": match_id,

            "home": bet["home"],
            "away": bet["away"],

            "status": "pending",
            "points": None,
            "updated_at": now,

            # snapshot
            "match_number": match["match_number"],
            "stage": match["stage"],
            "group_name": match["group_name"],

            "home_team": match["home_team"],
            "away_team": match["away_team"],

            "home_code": match["home_code"],
            "away_code": match["away_code"],

            "home_crest": match["home_crest"],
            "away_crest": match["away_crest"],

            "utc_date": match["utc_date"],
        })

    # 4. WRITE ONLY CHANGED
    if rows:
        supabase.table("bets").upsert(
            rows,
            on_conflict="username,match_id"
        ).execute()

    return {
        "changed": changed,
        "upserted": len(rows),
        "skipped": skipped
    }