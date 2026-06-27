from __future__ import annotations

from typing import Any

from app.core.db import get_supabase


def upsert_matches(rows: list[dict[str, Any]]) -> None:
    """Upsert normalized match rows into Supabase."""

    if not rows:
        return

    get_supabase().table("matches").upsert(rows, on_conflict="match_id").execute()
