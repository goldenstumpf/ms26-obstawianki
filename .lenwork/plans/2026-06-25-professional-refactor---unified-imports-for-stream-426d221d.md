---
plan_id: plan-426d221d
created: 2026-06-25T13:17:03.329229100+00:00
request: "We need to plan a proper refactoring, professionalisation of code, limiting redundancy, increasing the efficiency and eventually expanding and improving the streamlit UI. I am not able to access my personal github or authorise personal github in VSC, I also cannot use company github, so need some proper way of pushing it later."
status: approved
---

## Plan: Professional refactor + unified imports for Streamlit Cloud + Railway (no path hacks)

### Context
Your repo currently runs in two environments with different import roots: Streamlit Cloud runs the UI entrypoint in a way that makes imports like `from core...` / `from tabs...` work, while Railway runs the worker from repo root (`python -m app.worker.worker`) which naturally prefers `from app...`. This mixed approach is fragile and will keep breaking as the codebase grows. You also want a broader “professionalisation” refactor (less redundancy, better performance, cleaner architecture, better UI), and you can’t push to GitHub from this machine—so we need a practical “handoff” workflow (zip/email + push elsewhere).

### Approach
Make the project a proper Python package and standardize **all imports to one canonical form** (`from app...` everywhere), then make both deployments call the code in a way consistent with package execution. In parallel, introduce baseline engineering hygiene (tooling, configs, typing, logging, structure), then refactor data access to remove redundant queries and expensive merges, and finally reorganize the Streamlit UI into a scalable layout with caching and components. All changes will be staged in small, testable steps with explicit run commands for both Streamlit and the worker.

---

## Steps

1. **Baseline audit + target architecture**
   - What: Confirm current entrypoints, import styles, and runtime assumptions (Streamlit Cloud file path, Railway command, required secrets). Define the target “professional” structure and boundaries (UI vs domain vs data vs services).
   - Resources: `app/main.py`, `app/worker/worker.py`, `app/core/*`, `app/services/*`, `app/tabs/*`, `requirements.txt`
   - Output: A short architecture decision record (ADR-style) describing:
     - canonical import strategy (`app.*`)
     - entrypoints and how to run them
     - module boundaries

2. **Make packaging explicit (so imports work everywhere)**
   - What: Ensure `app/` is treated as a real package in all environments and define clean entrypoints.
     - keep `app/__init__.py` (already exists)
     - add/standardize a top-level UI entry module if needed (e.g., `streamlit_app.py` at repo root) that imports and runs `app.main`
   - Resources: repo root, `app/__init__.py`, Streamlit Cloud config expectations
   - Output: One consistent way to launch:
     - UI: `streamlit run streamlit_app.py` (or `streamlit run app/main.py` once imports are fixed)
     - worker: `python -m app.worker.worker`

3. **Unify imports across the entire codebase**
   - What: Replace *all* ambiguous-root imports with canonical package imports:
     - `from core...` → `from app.core...`
     - `from tabs...` → `from app.tabs...`
     - `from utils...` → `from app.utils...`
     - ensure services and UI both import from `app.*`
   - Resources: all `app/**/*.py`
   - Output: No more environment-dependent import behavior. Both Streamlit and Railway run from repo root without PYTHONPATH hacks.

4. **Fix requirements + runtime parity**
   - What: Fix `requirements.txt` (it is UTF-16LE right now and incomplete). Ensure dependencies match actual imports:
     - `streamlit`, `supabase`, `python-dateutil`
     - likely add: `requests` (used), `python-dotenv` (optional but used), and pin versions for stability
   - Resources: `requirements.txt`, code imports
   - Output: A clean, UTF-8 `requirements.txt` (or `pyproject.toml` if we go fully modern) that installs cleanly on Streamlit Cloud and Railway.

5. **Introduce “professional” project tooling (lightweight but real)**
   - What: Add basic static quality gates and structure:
     - formatting/linting: `ruff` (and optionally `black`)
     - typing: start with `pyright` (or mypy) in “basic” mode
     - pre-commit hooks (optional)
     - consistent logging setup (avoid `basicConfig` scattered everywhere)
   - Resources: new config files (e.g. `pyproject.toml`), minor edits in modules
   - Output: Repeatable code quality and fewer regressions during UI expansion.

6. **Refactor data access to reduce redundancy + improve efficiency**
   - What: The current `get_full_bets_info()` does a full “matches × users” cartesian merge in Python, which will get slow and memory-heavy as users/matches grow.
     - Define clear data access functions: “fetch matches”, “fetch bets for X”, “fetch scoreboard aggregate”, “fetch live view”.
     - Prefer server-side filtering/aggregation where possible (Supabase queries) and/or minimal client-side joins.
     - Add Streamlit caching (`st.cache_data`) for read-heavy calls with safe TTLs.
   - Resources: `app/core/bets.py`, `app/core/matches.py`, tabs that call them
   - Output: Faster UI + less DB load; a cleaner “data layer” API.

7. **Streamlit UI re-architecture for scalability**
   - What: Convert tabs into a more maintainable UI structure:
     - shared layout/components in `app/ui/components.py` (or keep in `app/utils/components.py` but formalize)
     - consistent session state management (auth, selected match, filters)
     - consistent i18n usage (you already have `app/core/i18n.py`)
     - plan improvements: better dashboard, live center improvements, admin tools, etc.
   - Resources: `app/tabs/*`, `app/utils/components.py`, `app/core/i18n.py`
   - Output: A UI that’s easier to extend without duplicating logic.

8. **Deployment alignment + runbooks (Streamlit Cloud + Railway)**
   - What: Provide exact settings/commands after refactor:
     - Streamlit Cloud: set “Main file path” to the chosen entrypoint; confirm Python version reality (Streamlit Cloud may not truly support 3.14 yet—this needs verification during execution).
     - Railway: keep `python -m app.worker.worker`
     - document required env vars/secrets and optional ones
   - Resources: README update, Streamlit/Railway settings
   - Output: A “how to deploy” guide and local run commands that match production.

9. **Practical “no-GitHub” handoff workflow for pushing later**
   - What: Since you can’t push from this machine:
     - keep work in git locally with clean commits
     - create a reproducible export bundle (zip) containing:
       - working tree
       - `.git` optional (if you want to preserve history) OR a patch file (`git format-patch`) that can be applied on a machine that *can* push
     - document step-by-step “apply patch and push” instructions for your remote machine
   - Resources: git history, packaging steps
   - Output: A reliable way to transfer changes to another machine and push without losing commit history.

---

### Key Decisions
- **Canonical imports:** Standardize on `from app...` everywhere. This is the “proper” Python packaging approach and eliminates path-dependent behavior.
- **Entrypoints:** Prefer running everything from repo root (`python -m ...` and `streamlit run ...`) rather than relying on Streamlit Cloud’s working-directory quirks.
- **Tooling choice:** Use `ruff` as the primary lint/format tool for low friction and speed.
- **Data layer direction:** Move away from cartesian merges and toward query/aggregation functions + caching.

---

### Expected Outcome
- The app runs **both** on Streamlit Cloud and on Railway worker with **no import/path issues**.
- A more maintainable, professional codebase: consistent package structure, proper dependency management, lint/format/type checks, clearer separation of UI/core/services.
- Better performance and easier future UI expansion.
- A documented workflow to transfer changes (zip/patch) and push from a different machine later.

If you approve this plan, I’ll start by implementing Steps 2–4 first (packaging + unified imports + requirements), then verify locally with the exact Streamlit + worker commands, before moving on to the deeper “professionalisation” refactors.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
