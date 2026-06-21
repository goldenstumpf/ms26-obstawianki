from datetime import datetime, timezone
from core.db import get_supabase
from typing import TypedDict, Any


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


def get_full_bets_info() -> list[dict]:
    """
    Returns full merged dataset:
    matches × bets (for all users).

    No filtering, no business logic.
    Pure data layer.
    """

    supabase = get_supabase()

    # ---------- matches ----------
    matches = (
        supabase.table("matches")
        .select("*")
        .execute()
        .data
        or []
    )

    # ---------- bets ----------
    bets = (
        supabase.table("bets")
        .select("*")
        .execute()
        .data
        or []
    )

    # ---------- build index ----------
    bets_by_key = {
        (b["username"], b["match_id"]): b
        for b in bets
    }

    # ---------- full cartesian merge ----------
    records = [
        {
            **match,
            **bets_by_key.get((user, match["match_id"]), {}),
            "username": user,
        }
        for match in matches
        for user in {b["username"] for b in bets}  # dynamic user list from bets
    ]

    records.sort(key=lambda r: int(r.get("match_number") or 0))
    return records

def apply_bets_filters(
    records: list[dict],
    filters: dict[str, Any] | None = None,
) -> list[dict]:
    """
    Generic filter layer over merged dataset.

    Supports filtering by ANY column present in merged records.
    """

    if not filters:
        return records

    result = records

    for key, value in filters.items():
        if value is None:
            continue

        # list filter → IN
        if isinstance(value, list):
            value_set = set(value)
            result = [
                r for r in result
                if r.get(key) in value_set
            ]
        else:
            result = [
                r for r in result
                if r.get(key) == value
            ]

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
) -> dict:
    """
    Saves user bets (clean version).

    Bets table is the single source of truth for:
    - username
    - match_id
    - home_bet
    - away_bet
    """

    supabase = get_supabase()
    now = datetime.now(timezone.utc).isoformat()

    # 1. existing bets for user
    existing_res = (
        supabase.table("bets")
        .select("match_id, home_bet, away_bet")
        .eq("username", username)
        .execute()
    )

    existing_map = {
        str(r["match_id"]): r
        for r in (existing_res.data or [])
    }

    rows = []
    skipped = 0
    changed = 0

    for match_id, bet in bets.items():

        # skip empty bets
        if bet.get("home_bet") is None or bet.get("away_bet") is None:
            skipped += 1
            continue

        existing = existing_map.get(str(match_id))

        new_bet = {
            "home_bet": bet["home_bet"],
            "away_bet": bet["away_bet"],
        }

        if existing and not _bet_changed(existing, new_bet):
            continue

        changed += 1

        rows.append({
            "username": username,
            "match_id": match_id,
            "home_bet": bet["home_bet"],
            "away_bet": bet["away_bet"],
            "points": None,
            "updated_at": now,
        })

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