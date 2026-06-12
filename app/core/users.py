from core.db import supabase


def authenticate(username, pin):

    res = (
        supabase
        .table("users")
        .select("pin")
        .eq("username", username)
        .execute()
    )

    if not res.data:
        return False

    return res.data[0]["pin"] == pin