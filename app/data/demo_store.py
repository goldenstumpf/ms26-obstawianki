from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_DEMO_DB_DIR = Path(__file__).resolve().parents[2] / "demo_db"


def _users_path() -> Path:
    return _DEMO_DB_DIR / "users.json"


def _matches_path() -> Path:
    return _DEMO_DB_DIR / "matches.json"


def _bets_path() -> Path:
    return _DEMO_DB_DIR / "bets.json"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(path)


def init_demo_db_if_missing(
    seed_users: list[dict],
    seed_matches: list[dict],
    seed_bets: list[dict],
) -> None:
    """Create demo_db JSON files if they do not exist.

    The app should call this only in DEMO_MODE.
    """

    _DEMO_DB_DIR.mkdir(parents=True, exist_ok=True)

    users_path = _users_path()
    matches_path = _matches_path()
    bets_path = _bets_path()

    if not users_path.exists():
        _write_json(users_path, seed_users)

    if not matches_path.exists():
        _write_json(matches_path, seed_matches)

    if not bets_path.exists():
        # ensure every bet row has updated_at
        bets = []
        for b in seed_bets:
            bb = dict(b)
            bb.setdefault("updated_at", _utc_now_iso())
            bets.append(bb)
        _write_json(bets_path, bets)


def load_users() -> list[dict[str, Any]]:
    return list(_read_json(_users_path()))


def load_matches() -> list[dict[str, Any]]:
    return list(_read_json(_matches_path()))


def load_bets() -> list[dict[str, Any]]:
    return list(_read_json(_bets_path()))


def save_bets(bets: list[dict[str, Any]]) -> None:
    _write_json(_bets_path(), bets)


def upsert_bets_for_user(username: str, bets: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Upsert bets for a user into the local demo_db/bets.json.

    Expected bets payload format:
      {match_id: {"home_bet": int|None, "away_bet": int|None, "dip": str|None}}

    Skips incomplete bets.
    """

    all_bets = load_bets()
    existing_idx = {
        (str(b.get("username")), str(b.get("match_id"))): i
        for i, b in enumerate(all_bets)
        if b.get("username") is not None and b.get("match_id") is not None
    }

    now = _utc_now_iso()
    skipped = 0
    changed = 0

    for match_id, bet in bets.items():
        hb = bet.get("home_bet")
        ab = bet.get("away_bet")
        if hb is None or ab is None:
            skipped += 1
            continue

        key = (str(username), str(match_id))
        row = {
            "username": username,
            "match_id": match_id,
            "home_bet": hb,
            "away_bet": ab,
            "dip": bet.get("dip"),
            "points": None,
            "status": "pending",
            "updated_at": now,
        }

        idx = existing_idx.get(key)
        if idx is None:
            all_bets.append(row)
            existing_idx[key] = len(all_bets) - 1
            changed += 1
        else:
            prev = all_bets[idx]
            if (
                prev.get("home_bet") == hb
                and prev.get("away_bet") == ab
                and prev.get("dip") == bet.get("dip")
            ):
                continue
            all_bets[idx] = {**prev, **row}
            changed += 1

    if changed:
        save_bets(all_bets)

    return {"changed": changed, "upserted": changed, "skipped": skipped}
