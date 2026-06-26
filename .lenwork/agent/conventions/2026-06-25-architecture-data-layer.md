# Architecture-data-layer Conventions

**Updated:** 2026-06-25 15:31 UTC

## Architecture / Data Layer

- DEMO_MODE feature: opt-in via env var `DEMO_MODE=1` read by `app/data/demo.py: demo_mode_enabled()`. When enabled, DAL functions in `app/data/users.py`, `app/data/matches.py`, `app/data/bets.py` must avoid all Supabase/network calls and instead use local fixtures from `app/data/fixtures.py` (demo_users/matches/bets). UI calls DAL unchanged.
