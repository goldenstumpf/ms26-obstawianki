from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.core.db import get_supabase
from app.data import demo_store
from app.data.demo import demo_mode_enabled


def list_bets(username: str | None = None) -> list[dict[str, Any]]:
    """Return bets (optionally filtered by username)."""

    if demo_mode_enabled():
        bets = demo_store.load_bets()
        if username is None:
            return bets
        return [b for b in bets if b.get("username") == username]

    query = get_supabase().table("bets").select("*")

    if username is not None:
        query = query.eq("username", username)

    res = query.execute()
    return res.data or []


def list_bets_map_for_user(username: str) -> dict[str, dict[str, Any]]:
    """Return {match_id -> bet} for a given user."""

    bets = list_bets(username=username)
    return {str(b["match_id"]): b for b in bets}


def upsert_bets_for_user(username: str, bets: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Upsert bet rows for a user.

    Expected bets payload format:
      {match_id: {"home_bet": int|None, "away_bet": int|None, "dip": str|None}}

    Skips incomplete bets (missing home/away).
    """

    now = datetime.now(timezone.utc).isoformat()

    # demo mode: persist to local JSON store
    if demo_mode_enabled():
        return demo_store.upsert_bets_for_user(username=username, bets=bets)

    supabase = get_supabase()

    # fetch existing so we can avoid unnecessary writes
    existing_res = (
        supabase.table("bets")
        .select("match_id, home_bet, away_bet, dip")
        .eq("username", username)
        .execute()
    )

    existing_map = {str(r["match_id"]): r for r in (existing_res.data or [])}

    rows: list[dict[str, Any]] = []
    skipped = 0
    changed = 0

    for match_id, bet in bets.items():
        if bet.get("home_bet") is None or bet.get("away_bet") is None:
            skipped += 1
            continue

        prev = existing_map.get(str(match_id))
        if (
            prev
            and prev.get("home_bet") == bet.get("home_bet")
            and prev.get("away_bet") == bet.get("away_bet")
            and prev.get("dip") == bet.get("dip")
        ):
            continue

        changed += 1
        rows.append(
            {
                "username": username,
                "match_id": match_id,
                "home_bet": bet.get("home_bet"),
                "away_bet": bet.get("away_bet"),
                "dip": bet.get("dip"),
                "points": None,
                "updated_at": now,
            }
        )

    if rows:
        supabase.table("bets").upsert(rows, on_conflict="username,match_id").execute()

    return {"changed": changed, "upserted": len(rows), "skipped": skipped}


def list_active_bets() -> list[dict[str, Any]]:
    """Return bets that are not closed."""

    if demo_mode_enabled():
        return [b for b in demo_store.load_bets() if b.get("status") != "closed"]

    res = (
        get_supabase()
        .table("bets")
        .select("*")
        .neq("status", "closed")
        .execute()
    )
    return res.data or []
