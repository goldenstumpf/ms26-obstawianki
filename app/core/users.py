from typing import Optional, TypedDict
from core.db import supabase


# =========================
# MODEL (opcjonalny, ale pomaga)
# =========================

class User(TypedDict):
    username: str
    pin: str


# =========================
# AUTH
# =========================

def authenticate(username: str, pin: str) -> bool:
    """
    Authenticates user using username + PIN.

    Args:
        username: user identifier
        pin: plain PIN (simple auth system)

    Returns:
        bool: True if credentials are valid
    """

    if not username or not pin:
        return False

    res = (
        supabase
        .table("users")
        .select("pin")
        .eq("username", username)
        .limit(1)
        .execute()
    )

    data = res.data or []

    if not data:
        return False

    return data[0]["pin"] == pin


# =========================
# USER FETCH (optional helper)
# =========================

def get_user(username: str) -> Optional[User]:
    """
    Fetches user data (if needed for UI or future features).
    """

    res = (
        supabase
        .table("users")
        .select("*")
        .eq("username", username)
        .limit(1)
        .execute()
    )

    data = res.data or []

    if not data:
        return None

    return data[0]


# =========================
# EXISTENCE CHECK
# =========================

def user_exists(username: str) -> bool:
    """
    Checks if user exists in DB.
    """

    res = (
        supabase
        .table("users")
        .select("username")
        .eq("username", username)
        .limit(1)
        .execute()
    )

    return bool(res.data)