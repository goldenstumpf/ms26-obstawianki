---
plan_id: plan-27672458
created: 2026-06-26T06:36:35.412826400+00:00
request: "Yes, I want a \"repo professionaliztion pass\". Set the goals and review all the files to align with them."
status: approved
---

## Plan: Repo professionalization pass (Streamlit UI + Railway worker)

### Context
You want the repository to be “professionally maintainable”: consistent architecture, clear boundaries (UI vs data access vs services), predictable imports across environments, and reliable local dev (including DEMO_MODE for Streamlit only). You also want to remove redundant/legacy layers (especially `app/core` duplication) and drop the unused GitHub workflow since you’re using Railway.

### Approach
I’ll define concrete “done” goals, then do a repo-wide audit and refactor plan centered on **one canonical data-access layer (`app/data`)**, **package-safe imports (`from app...`)**, and **clean deploy targets** (Streamlit Cloud UI + Railway worker). I’ll also standardize Python to **3.11** across config/docs and make DEMO_MODE explicitly a **UI-only** feature. Tooling (ruff/pre-commit/tests) is optional; I’ll explain what each does and include it as a selectable step in the plan.

---

### Goals (“done” criteria)
1. **Single-source architecture**
   - `app/data` is the only DAL (Supabase + DEMO JSON).
   - `app/services` uses DAL only (no direct Supabase calls unless clearly justified).
   - `app/tabs` (Streamlit UI) uses DAL only.
   - `app/core` is removed or reduced to truly “core” utilities only (no DB access duplication).

2. **Import correctness**
   - No `core.*`, `utils.*`, `tabs.*`, `data.*` imports anywhere.
   - Everything imports via `app.*` so it runs identically on Streamlit Cloud, Railway, and locally.

3. **Environment clarity**
   - Python **3.11** is the declared target (docs + config).
   - DEMO_MODE only affects the Streamlit UI paths (worker stays production-like).
   - No hidden side effects at import-time (especially for worker).

4. **Deploy/readme correctness**
   - README reflects *current* behavior (DEMO uses `demo_db/*.json`, not “fixtures”).
   - Railway worker command is clear and minimal.
   - Streamlit entrypoint remains `streamlit_app.py`.

5. **Remove unused automation**
   - Remove `.github/workflows/update_db.yml` since you’re not using GitHub Actions for this.

---

### Steps
1. **Repo-wide inventory + dependency map**
   - What: Enumerate all modules and build a simple dependency/ownership map: who calls DAL, who calls Supabase, where DEMO_MODE branches exist.
   - Resources: `glob app/**/*.py`, `grep get_supabase|create_client|DEMO_MODE`, read key modules (`app/services/*`, `app/tabs/*`, `app/data/*`, `app/core/*`).
   - Output: A short “current architecture” report + list of concrete refactor targets.

2. **Unify data access: migrate `app/core` callers to `app/data`**
   - What: Replace usages of `app.core.matches/users/bets` with equivalent `app.data.*` calls; ensure services and UI depend only on DAL.
   - Resources: `app/core/*.py`, `app/data/*.py`, `app/services/*.py`, `app/tabs/*.py`.
   - Output: `app/core/{matches,users,bets}.py` removed (or reduced to re-export wrappers temporarily, then removed).

3. **Fix remaining non-package imports**
   - What: Fix `app/tabs/_experimental_dashboard.py` imports (`core.*` → `app.data`/`app.utils`) or remove the file if not used.
   - Resources: `app/tabs/_experimental_dashboard.py`, `app/tabs/__init__.py`, `app/main.py` (to see if it’s referenced).
   - Output: `grep` for non-package imports returns zero.

4. **Make DEMO_MODE explicitly UI-only**
   - What: Ensure DEMO_MODE is checked only in DAL functions used by UI (already mostly true), and confirm worker/services do not accidentally branch into demo.
   - Resources: `app/data/demo.py`, DAL modules, `app/worker/worker.py`, `app/services/*`.
   - Output: A clear contract: “DEMO_MODE is for Streamlit UI local dev only”.

5. **Standardize Python 3.11**
   - What: Update `pyproject.toml` target-version to `py311` and add any metadata needed (optionally).
   - Resources: `pyproject.toml`, README.
   - Output: Consistent Python 3.11 target across docs/config.

6. **Remove unused GitHub Actions workflow**
   - What: Delete `.github/workflows/update_db.yml` (and possibly `.github/` if empty afterwards).
   - Resources: `.github/workflows/update_db.yml`.
   - Output: Repo no longer suggests GitHub Actions pipeline.

7. **Docs + runbook cleanup**
   - What: Update README wording: DEMO uses `demo_db/*.json`; explain local setup; explicitly list Streamlit Cloud + Railway worker run commands; clarify secrets.
   - Resources: `README.md`, maybe add `docs/` or keep in README.
   - Output: “Single source of truth” docs that match actual code.

8. **Optional: Add professional dev tooling (you decide after explanation)**
   - What (if enabled):
     - **ruff**: fast linter + import sorter (already partially configured in `pyproject.toml`).
     - **pre-commit**: runs ruff automatically before commits (prevents style regressions).
     - **pytest**: minimal tests for DAL demo behavior + import sanity.
   - Resources: `pyproject.toml`, add `.pre-commit-config.yaml`, add `tests/`.
   - Output: Automated guardrails so the repo stays clean over time.

9. **Verification**
   - What: Run a small checklist of commands:
     - `python -c "import streamlit_app; import app.main; import app.worker.worker"`
     - `streamlit run streamlit_app.py` (smoke)
     - `DEMO_MODE=1` smoke (UI-side DAL calls)
     - worker import/run sanity (without DEMO)
   - Output: Confirmed working UI + worker; no import/path issues.

---

### Key Decisions (based on your answers)
- **Remove redundant layers**: We will eliminate `app/core` DB/DAL duplication and keep a single DAL under `app/data`.
- **No DEMO for worker**: DEMO_MODE is only for Streamlit UI/local testing.
- **Standardize to Python 3.11**: Update config/docs accordingly.
- **GitHub workflow not needed**: Remove GitHub Actions pipeline file.

---

### Expected Outcome
A cleaned-up repo with:
- One clear architecture (UI → DAL, worker/services → DAL),
- Zero environment-dependent imports,
- Python 3.11 alignment,
- DEMO_MODE supported for Streamlit UI local dev without affecting production/worker,
- Removed unused GitHub Actions workflow,
- Documentation that matches how the repo actually runs.

If you answer the remaining tooling question (“ruff/pre-commit/pytest”: do you want automated guardrails or just code+docs cleanup), I’ll finalize this plan into an execution-ready checklist with exact file changes and verification commands.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
