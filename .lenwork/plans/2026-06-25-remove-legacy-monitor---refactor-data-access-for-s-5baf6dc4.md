---
plan_id: plan-5baf6dc4
created: 2026-06-25T14:19:33.568901600+00:00
request: "We need to review the efficiency and professionalism of core modules and services and later focus on UI by improving the current one and extending the tabs to provide full experience for the users"
status: approved
---

## Plan: Remove legacy monitor + refactor data access for scalability + enable hands‑on UI testing

### Context
You confirmed:
- `app/services/monitor.py` can be removed (good; it’s legacy and buggy).
- `submit_bets` should be adjusted (it currently depends on heavy merged datasets).
- `dashboard` is redundant/unusable (HTML rendering issues) and can be removed or parked.
- You need a practical way to **test the UI hands-on** during refactors.

Goal: make core/services scalable for new analytics tabs, while keeping the Streamlit app easy to run locally (or in a shared “test” deployment) for iterative UI work.

### Approach
1) Clean up legacy code (remove `monitor`, retire `dashboard` cleanly).
2) Introduce a **thin data-access layer** so UI tabs pull *only what they need* (no `matches × users` cartesian merge).
3) Refactor `submit_bets` to use the new data functions and Streamlit caching.
4) Add a reliable hands-on testing workflow: local “dev run” + optional “test mode” + optional staging deployment checklist.

---

## Steps

1. **Remove/retire unused legacy modules safely**
   - What:
     - Delete `app/services/monitor.py` (and ensure nothing imports it).
     - Decide what to do with `app/tabs/dashboard.py`:
       - Option A: remove it entirely
       - Option B: keep it as `app/tabs/_experimental_dashboard.py` and exclude from menu
   - Resources: `app/services/monitor.py`, `app/tabs/dashboard.py`, `app/main.py` menu
   - Output: No dead code confusing future refactors; simpler mental model.

2. **Create a proper data-access layer (DAL)**
   - What: Add a package like `app/data/` (or `app/repos/`) with small, testable functions:
     - `matches.py`: `list_matches()`, `list_bettable_matches(hours=72)`, `list_live_matches()`, `get_next_match()`
     - `bets.py`: `list_bets_for_user(username)`, `upsert_bets(username, payload)`, `list_active_bets()`
     - `users.py`: `get_user_pin(username)` / `authenticate_user(...)`
   - Add Streamlit-friendly cached wrappers (`st.cache_data`) for read operations with TTL.
   - Resources: current query code in `app/core/*`, Supabase schema
   - Output: UI calls DAL instead of mixing query + business logic.

3. **Refactor `submit_bets` to stop using `get_full_bets_info()`**
   - What:
     - Replace the pattern “fetch everything then filter” with:
       - fetch bettable matches (100 max)
       - fetch this user’s bets only
       - merge in memory by `match_id`
     - Keep current UX (unbet/bet sections, session_state handling) but reduce coupling and complexity.
   - Resources: `app/tabs/submit_bets.py`, `app/utils/components.py`, new DAL modules
   - Output: Faster reruns, easier future analytics, less redundant code.

4. **Consolidate / simplify core modules**
   - What:
     - Convert `app/core/*` into either:
       - domain logic only (pure functions), while DAL owns DB calls, **or**
       - keep `core` as “service layer” but enforce clear boundaries and naming.
     - Reduce redundancy: avoid multiple “get_supabase().table(...).select('*')” scattered everywhere.
   - Resources: `app/core/bets.py`, `app/core/matches.py`, `app/core/users.py`
   - Output: A scalable architecture for adding analytics.

5. **Hands-on UI testing workflow (must-have)**
   - What: Provide 2 practical ways to test:
     1) **Local dev run** (primary):
        - `pip install -r requirements.txt`
        - set env vars in a local `.env`
        - `streamlit run streamlit_app.py`
     2) **UI test mode** (optional but powerful):
        - add a `DEMO_MODE=1` option that uses small in-memory fixtures instead of Supabase,
          so you can develop analytics tabs without touching production data.
        - alternatively, a “staging schema” in Supabase if you prefer real DB testing.
   - Resources: `streamlit_app.py`, `app/core/db.py` (secret loading), new fixture module if DEMO_MODE
   - Output: You can iterate on UI safely and quickly.

6. **Prepare analytics foundation for future tabs**
   - What: Add `app/analytics/` with pure functions operating on “matches + bets” datasets:
     - team-based leaderboard
     - “best predictors per team”
     - what-if group standings vs reality
     - rules tab content
   - Resources: new DAL outputs + existing scoring rules in `app/services/score_bets.py`
   - Output: Clean base for new “full experience” tabs.

---

## Key Decisions
- **Remove monitor** entirely; keep only `app/worker/worker.py` as the worker loop.
- **Stop using `get_full_bets_info()` for UI** where not strictly needed.
- For hands-on UI testing: prefer **local run**, plus optional **DEMO_MODE** for safe iteration.

---

## Expected Outcome
- Cleaner repo: no dead monitor, no redundant dashboard in the menu.
- `submit_bets` becomes scalable and easier to modify.
- A maintainable foundation (DAL + core separation) ready for analytics tabs.
- You can test UI hands-on locally (and optionally in demo mode) during development.

If you confirm whether you prefer **DEMO_MODE fixtures** or **a staging Supabase schema**, I’ll make the plan’s Step 5 concrete (exact file layout + how to toggle it).

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
