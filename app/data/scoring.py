from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.core.db import get_supabase


def fetch_matches_map(match_ids: list[str]) -> dict[str, dict[str, Any]]:
    """Batch fetch matches and return map: match_id -> match row."""

    if not match_ids:
        return {}

    res = (
        get_supabase()
        .table("matches")
        .select("*")
        .in_("match_id", match_ids)
        .execute()
    )

    return {str(m["match_id"]): m for m in (res.data or [])}


def update_bet_row(username: str, match_id: str, *, status: str, points: float | None) -> None:
    """Update a single bet row (status, points, updated_at)."""

    get_supabase().table("bets").update(
        {
            "status": status,
            "points": points,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("username", username).eq("match_id", match_id).execute()
