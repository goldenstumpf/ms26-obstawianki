from __future__ import annotations

 

from typing import Any

 

from app.core.db import get_supabase

from app.data.bets import list_bets

from app.data.matches import list_matches

 

 

def _norm(value: Any) -> str | None:

    if value is None:

        return None

    text = str(value).strip()

    return text or None

 

 

def list_usernames() -> list[str]:

    res = get_supabase().table("users").select("username").execute()

    rows = res.data or []

    return sorted(

        {

            _norm(r.get("username"))

            for r in rows

            if _norm(r.get("username")) is not None

        }

    )

 

 

def get_full_bets_info() -> list[dict[str, Any]]:

    matches = list_matches()

    usernames = list_usernames()

 

    bets: list[dict[str, Any]] = []

    for username in usernames:

        bets.extend(list_bets(username=username))

 

    bets_by_key = {

        (_norm(b.get("username")), _norm(b.get("match_id"))): b

        for b in bets

        if _norm(b.get("username")) is not None

        and _norm(b.get("match_id")) is not None

    }

 

    records: list[dict[str, Any]] = []

    for match in matches:

        mid = _norm(match.get("match_id"))

        for user in usernames:

            records.append({

                **match,

                **bets_by_key.get((user, mid), {}),

                "username": user,

            })

 

    records.sort(key=lambda r: int(r.get("match_number") or 0))

    return records