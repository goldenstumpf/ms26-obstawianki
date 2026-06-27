from __future__ import annotations

from typing import Any


def apply_bets_filters(
    records: list[dict[str, Any]],
    filters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Generic filter layer over merged dataset.

    This is a small utility used by the UI to filter merged records by any field.
    Kept in app.data so DEMO_MODE does not depend on app.core.
    """

    if not filters:
        return records

    result: list[dict[str, Any]] = records

    for key, value in filters.items():
        if value is None:
            continue

        if isinstance(value, list):
            value_set = set(value)
            result = [r for r in result if r.get(key) in value_set]
        else:
            result = [r for r in result if r.get(key) == value]

    return result
