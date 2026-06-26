from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.db import get_supabase
from app.data import demo_store
from app.data.demo import demo_mode_enabled
from app.utils.time import parse_kickoff


def list_matches() -> list[dict[str, Any]]:
    """Return all matches ordered by kickoff time."""

    if demo_mode_enabled():
        matches = demo_store.load_matches()
        matches.sort(key=lambda m: m.get("utc_date") or "")
        return matches

    res = (
        get_supabase()
        .table("matches")
        .select("*")
        .order("utc_date")
        .execute()
    )

    return res.data or []


def list_bettable_matches(hours: int = 72) -> list[dict[str, Any]]:
    """Return matches that are within the betting window (now → now+hours)."""

    matches = list_matches()

    now = datetime.now(timezone.utc)
    limit = now + timedelta(hours=hours)

    result: list[dict[str, Any]] = []

    for m in matches:
        if not m.get("home_team") or not m.get("away_team"):
            continue

        utc_date = m.get("utc_date")
        if not utc_date:
            continue

        match_time = parse_kickoff(utc_date)

        if now <= match_time <= limit:
            result.append(m)

    return result


LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT",
    "LIVE",
}


def list_live_matches() -> list[dict[str, Any]]:
    """Return live matches."""

    if demo_mode_enabled():
        return [m for m in demo_store.load_matches() if m.get("status") in LIVE_STATUSES]

    res = (
        get_supabase()
        .table("matches")
        .select("*")
        .in_("status", list(LIVE_STATUSES))
        .execute()
    )
    return res.data or []


def get_next_match() -> dict[str, Any] | None:
    """Return the next scheduled match (with a small grace window)."""

    now = (datetime.now(timezone.utc) - timedelta(minutes=15)).isoformat()

    if demo_mode_enabled():
        future = [m for m in demo_store.load_matches() if (m.get("utc_date") or "") > now]
        future.sort(key=lambda m: m.get("utc_date") or "")
        return future[0] if future else None

    res = (
        get_supabase()
        .table("matches")
        .select("*")
        .gt("utc_date", now)
        .order("utc_date")
        .limit(1)
        .execute()
    )

    return (res.data or [None])[0]
