---
plan_id: plan-8d237c14
created: 2026-06-26T07:09:44.729815100+00:00
request: "Create a prioritized repo professionalization checklist and apply it across the codebase, including naming, structure, docs, tests, CI, and dependency hygiene."
status: approved
---

## Plan: Repo professionalization checklist + apply across codebase (Python 3.11, minimal tests, local checks)

### Context
You want a **prioritized professionalization checklist** and then to **apply it repo-wide**: naming, structure, docs, tests, dependency hygiene, and “CI-like” quality gates—but with your constraint that you prefer **no hosted CI**, only **local checks**. The repo is a Streamlit UI + a Railway worker, with a required **DEMO_MODE** that is network-free and JSON-backed (`demo_db/`).

### Approach
I’ll start by producing a **prioritized checklist** grouped by impact (P0/P1/P2), then execute it in small batches: (1) architecture/structure cleanup, (2) naming + module boundaries (especially the duplicated `app/core/*` vs `app/data/*` Supabase access), (3) docs consolidation, (4) minimal tests (pytest) focused on DEMO_MODE + import/package integrity, and (5) dependency/tooling hygiene with an easy local “CI replacement” command (`python -m ...` / `ruff` / `pytest`). Changes will keep **package-safe imports** (`app.*`) and preserve production behavior.

### Steps
1. **Create the prioritized checklist (P0/P1/P2)**
   - What: Write a `docs/professionalization-checklist.md` (or add to README) capturing concrete items and acceptance criteria (what “done” means).
   - Resources: current repo structure; `README.md`, `pyproject.toml`, `requirements.txt`.
   - Output: A single source of truth checklist you can track.

2. **Structure + naming cleanup (low-risk, high clarity)**
   - What:
     - Add top-level folders: `tests/`, `docs/`, optionally `scripts/`.
     - Add/adjust `__all__`/module docstrings where helpful.
     - Normalize naming (e.g., “DAL” naming, “services” vs “worker” responsibilities).
   - Resources: `app/` tree, existing module names, `.gitignore`.
   - Output: Clearer repo layout without changing runtime behavior.

3. **Data access boundary: remove duplication (`app/core/*` vs `app/data/*`)**
   - What:
     - Decide and enforce: **only `app/data/*` talks to Supabase/demo_store**.
     - Move/merge the duplicated Supabase query code currently living in `app/core/bets.py`, `app/core/users.py`, `app/core/matches.py` into `app/data/*`.
     - Update imports so UI tabs and worker depend on `app.data.*` not `app.core.*` for DB access.
   - Resources: `app/core/db.py`, `app/core/*`, `app/data/*`, `app/worker/worker.py`, `app/services/*`.
   - Output: One DAL, less drift, DEMO_MODE stays centralized.

4. **Docs upgrade (beyond README)**
   - What: Add short docs:
     - `docs/runbook.md` (local run, deploy notes, DEMO_MODE, troubleshooting SSL/proxy)
     - `docs/architecture.md` (module boundaries: tabs vs services vs data vs worker)
   - Resources: README + discovered repo conventions.
   - Output: New contributors (or future you) can onboard fast.

5. **Minimal tests (smoke/unit) + local “CI replacement” commands**
   - What:
     - Add `pytest` and create a small test suite:
       - Import/package safety test: `import app`, `import app.main`, worker import
       - DEMO_MODE test: `DEMO_MODE=1` → uses demo_store (no Supabase calls) and basic read/write works
       - A couple of pure-function unit tests (e.g., scoring filters) if applicable
     - Add a `scripts/check.ps1` (Windows) or `python -m` entry that runs:
       - `ruff check .`
       - `python -m pytest -q`
   - Resources: `pyproject.toml` (ruff already present), add pytest configuration.
   - Output: Reliable local quality gate you can run before deploying or sharing.

6. **Dependency hygiene**
   - What:
     - Split deps: keep `requirements.txt` for runtime; add `requirements-dev.txt` (pytest, ruff, etc.) or manage dev deps in `pyproject.toml`.
     - Pin where appropriate (at least major/minor) to reduce “works on my machine”.
     - Fix `.gitignore` entries that look stale (e.g. `data/users.json` vs current `demo_db/`).
   - Resources: `requirements.txt`, `.gitignore`, current imports.
   - Output: Cleaner installs, fewer surprises.

7. **Final verification**
   - What:
     - Run the local check script.
     - Quick manual smoke: `streamlit run streamlit_app.py` with and without `DEMO_MODE=1` (as far as possible here), ensure worker still starts.
   - Resources: local commands + targeted greps.
   - Output: “Professionalized” repo with a repeatable validation workflow.

### Key Decisions
- **Python 3.11** is the standardized target (tooling + docs will reflect that).
- **No hosted CI**: we’ll implement **local CI-equivalent checks** (script + documented commands).
- Repo structure: we’ll choose the robust option: add `tests/` + `docs/` (and optionally `scripts/`), while keeping runtime code under `app/`.
- Formatting/tooling enforcement: I’ll propose a pragmatic default:
  - enable `ruff check` + (optionally) `ruff format`
  - pre-commit can be added but left optional unless you explicitly want enforcement.

### Expected Outcome
- A tracked, prioritized checklist committed into the repo.
- A cleaner module boundary (single DAL), consistent naming/structure, improved docs.
- A minimal but meaningful test suite and a simple local “CI replacement” command/script.
- Reduced dependency drift and fewer environment-specific breakages (Streamlit Cloud + Railway + local DEMO_MODE).

If you approve this plan, I’ll start by generating the checklist doc (P0/P1/P2) and then execute items in that order with small, verifiable commits.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
