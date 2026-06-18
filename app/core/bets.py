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
    Upsert bets for user.

    Returns:
        dict with:
        - inserted: int
        - updated: int
        - skipped: int
    """

    now = datetime.now(timezone.utc).isoformat()

    rows = []
    skipped = 0

    match_map = {str(m["match_id"]): m for m in matches}

    for match_id, bet in bets.items():
        match = match_map.get(match_id)
        if not match:
            skipped += 1
            continue

        home = bet.get("home")
        away = bet.get("away")

        if home is None or away is None:
            skipped += 1
            continue

        rows.append({
            "username": username,
            "match_id": match_id,

            "home": home,
            "away": away,

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

    if not rows:
        return {
            "inserted": 0,
            "updated": 0,
            "skipped": skipped
        }

    res = supabase.table("bets").upsert(
        rows,
        on_conflict="username,match_id"
    ).execute()

    # Supabase nie daje łatwo insert/update split → traktujemy jako upsert batch
    return {
        "inserted": len(rows),
        "updated": len(rows),
        "skipped": skipped
    }

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

            # USER BET
            "home": home,
            "away": away,

            # MATCH SNAPSHOT (NOWE)
            "match_number": match["match_number"],
            "stage": match["stage"],
            "group_name": match["group_name"],
            "home_team": match["home_team"],
            "away_team": match["away_team"],
            "home_code": match["home_code"],
            "away_code": match["away_code"],
            "home_crest": match["home_crest"],
            "away_crest": match["away_crest"],

            # INIT STATE
            "status": "pending",
            "points": None,

            "updated_at": now.isoformat(),

            "utc_date": match["utc_date"]
        })

        saved += 1

    if rows:
        supabase.table("bets").upsert(
            rows,
            on_conflict="username,match_id"
        ).execute()

    return saved

def get_total_table():
    res = (
        supabase.table("bets")
        .select("username, points")
        .eq("status", "closed")
        .execute()
    )

    bets = res.data or []

    stats = {}

    for bet in bets:
        username = bet["username"]

        if username not in stats:
            stats[username] = {
                "username": username,
                "bets": 0,
                "points": 0.0
            }

        stats[username]["bets"] += 1
        stats[username]["points"] += bet.get("points") or 0

    rows = []

    for row in stats.values():
        rows.append({
            "username": row["username"],
            "bets": row["bets"],
            "points": row["points"],
            "avg": round(row["points"] / row["bets"], 2)
        })

    rows.sort(key=lambda x: x["points"], reverse=True)

    return rows