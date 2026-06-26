# Architecture Conventions

**Updated:** 2026-06-25 12:28 UTC

## Architecture

- Repo is a Streamlit app with entrypoint app/main.py. Structure: app/tabs/ (UI screens like login/submit bets/tables/live center/reports), app/core/ (domain + data access: users, matches, bets, config, db), app/services/ (background jobs: fetching matches, scoring, monitoring), app/worker/ (wrapper for background tasks), app/utils/ (helpers). App relates to collecting/scoring bets and reporting ("Zielone Zakłady 2026").
- Refactor decisions implemented: removed legacy app/services/monitor.py; retired app/tabs/dashboard.py as app/tabs/_experimental_dashboard.py (not in menu). Introduced a Data Access Layer under app/data (matches.py, bets.py, users.py) to avoid heavy global merged datasets; refactored submit_bets tab to fetch only bettable matches + current user's bets and merge in-memory by match_id; added DEMO_MODE with fixtures (app/data/demo.py, app/data/fixtures.py) for hands-on UI testing without Supabase; login uses DAL authenticate_user so DEMO_MODE works end-to-end.
- Project has legacy Supabase-calling layer under `app/core/*` (e.g., `app/core/bets.py:get_full_bets_info()` using postgrest/httpx) and a newer demo-safe DAL under `app/data/*` gated by `DEMO_MODE`. Some Streamlit tabs were still using `app/core/*`, causing SSL failures in demo mode.
