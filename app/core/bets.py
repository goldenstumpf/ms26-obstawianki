from datetime import datetime, timezone
from core.db import get_supabase
from typing import TypedDict


# =========================
# MODELS
# =========================


class BetInput(TypedDict):
    home_bet: int | None
    away_bet: int | None

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

    home_bet: int | None
    away_bet: int | None

    status: str
    points: float | None

    updated_at: str

class FullBetInfo(TypedDict):
    username: str
    match_id: str

    home_bet: int | None
    away_bet: int | None

    status: str
    points: float | None

    updated_at: str

    # Match Snapshot
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

    query = get_supabase().table("bets").select("*")

    if isinstance(username, str):
        query = query.eq("username", username)

    elif isinstance(username, list):
        query = query.in_("username", username)

    res = query.execute()
    return res.data or []


def get_full_bets_info(
    username: str | list[str] | None = None,
) -> list[FullBetInfo]:
    """
    Fetch matches enriched with bet information.

    Args:
        username:
            - None -> all users
            - str -> single user
            - list[str] -> multiple users

    Returns:
        List of match+bet records.

        For a specific user, returns all matches (including those without bets).

        For multiple users / all users, returns a row for every
        (user, match) combination, including missing bets.
    """

    supabase = get_supabase()

    matches = (
        supabase.table("matches")
        .select("*")
        .execute()
        .data
        or []
    )

    bets_query = supabase.table("bets").select("*")

    if isinstance(username, str):
        bets_query = bets_query.eq("username", username)

    elif isinstance(username, list):
        bets_query = bets_query.in_("username", username)

    bets = bets_query.execute().data or []

    # Single-user case
    if isinstance(username, str):
        bets_by_match = {
            bet["match_id"]: bet
            for bet in bets
        }

        result = []

        for match in matches:
            bet = bets_by_match.get(match["match_id"], {})

            result.append({
                **match,
                **bet,
                "username": username,
            })

        return result

    # Multi-user / all-users case
    usernames = (
        username
        if isinstance(username, list)
        else sorted({bet["username"] for bet in bets})
    )

    bets_by_key = {
        (bet["username"], bet["match_id"]): bet
        for bet in bets
    }

    result = []

    for user in usernames:
        for match in matches:
            bet = bets_by_key.get(
                (user, match["match_id"]),
                {},
            )

            result.append({
                **match,
                **bet,
                "username": user,
            })

    return result

# =========================
# WRITE
# =========================

def _bet_changed(existing: dict, new: dict) -> bool:
    return (
        existing.get("home_bet") != new.get("home_bet")
        or existing.get("away_bet") != new.get("away_bet")
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
        get_supabase().table("bets")
        .select("match_id, home_bet, away_bet")
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

        if bet.get("home_bet") is None or bet.get("away_bet") is None:
            skipped += 1
            continue

        existing = existing_map.get(match_id)

        new_bet = {
            "home_bet": bet["home_bet"],
            "away_bet": bet["away_bet"],
        }

        # 3. DIFF CHECK
        if existing and not _bet_changed(existing, new_bet):
            continue  # no real change

        changed += 1

        rows.append({
            "username": username,
            "match_id": match_id,

            "home_bet": bet["home_bet"],
            "away_bet": bet["away_bet"],

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
        get_supabase().table("bets").upsert(
            rows,
            on_conflict="username,match_id"
        ).execute()

    return {
        "changed": changed,
        "upserted": len(rows),
        "skipped": skipped
    }