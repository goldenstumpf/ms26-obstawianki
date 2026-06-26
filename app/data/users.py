from __future__ import annotations

from typing import Any

from app.core.db import get_supabase
from app.data import demo_store
from app.data.demo import demo_mode_enabled


def get_user_pin(username: str) -> str | None:
    """Return stored PIN for a user, or None if user not found."""

    if demo_mode_enabled():
        for u in demo_store.load_users():
            if u.get("username") == username:
                return u.get("pin")
        return None

    res = (
        get_supabase()
        .table("users")
        .select("pin")
        .eq("username", username)
        .limit(1)
        .execute()
    )

    data = res.data or []
    if not data:
        return None

    return data[0].get("pin")


def authenticate_user(username: str, pin: str) -> bool:
    """Authenticate user by username + PIN."""

    if not username or not pin:
        return False

    stored = get_user_pin(username)
    return stored == pin


def list_users() -> list[dict[str, Any]]:
    """Return all users (mainly for admin/analytics)."""

    if demo_mode_enabled():
        return demo_store.load_users()

    res = get_supabase().table("users").select("*").execute()
    return res.data or []
