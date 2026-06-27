from pathlib import Path


def test_demo_mode_demo_store_roundtrip(tmp_path: Path, monkeypatch) -> None:
    # Enable DEMO_MODE and point demo_store at a temp demo_db folder
    monkeypatch.setenv("DEMO_MODE", "1")

    # Import after setting env var
    from app.data import demo_store

    demo_dir = tmp_path / "demo_db"
    demo_dir.mkdir(parents=True, exist_ok=True)

    # Monkeypatch module-level path
    monkeypatch.setattr(demo_store, "_DEMO_DB_DIR", demo_dir)

    # Seed and initialize
    users = [{"username": "alice", "pin": "1111"}]
    matches = [
        {
            "match_id": "1",
            "match_number": 1,
            "utc_date": "2099-01-01T00:00:00+00:00",
            "status": "SCHEDULED",
        }
    ]
    bets = []

    demo_store.init_demo_db_if_missing(seed_users=users, seed_matches=matches, seed_bets=bets)

    loaded_users = demo_store.load_users()
    assert loaded_users[0]["username"] == "alice"

    # Upsert a bet and verify persistence
    result = demo_store.upsert_bets_for_user(
        username="alice",
        bets={"1": {"home_bet": 1, "away_bet": 2}},
    )
    assert result["upserted"] == 1

    loaded_bets = demo_store.load_bets()
    assert any(b.get("username") == "alice" and str(b.get("match_id")) == "1" for b in loaded_bets)
