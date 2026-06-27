from __future__ import annotations

from typing import Any

from app.data.bets import list_bets
from app.data.matches import list_matches


def get_full_bets_info() -> list[dict[str, Any]]:
    """Return full merged dataset: matches × bets (for all users).

    This is the DAL replacement for app.core.bets.get_full_bets_info.

    In DEMO_MODE, list_matches/list_bets already return demo_db JSON data via demo_store,
    so this function remains network-free.
    """

    matches = list_matches()
    bets = list_bets(username=None)

    bets_by_key = {(b.get("username"), b.get("match_id")): b for b in bets}
    users = {b.get("username") for b in bets if b.get("username")}

    records: list[dict[str, Any]] = []
    for match in matches:
        mid = match.get("match_id")
        for user in users:
            record = {**match, **bets_by_key.get((user, mid), {}), "username": user}
            records.append(record)

    records.sort(key=lambda r: int(r.get("match_number") or 0))
    return records
