# Repo professionalization checklist (ms26-obstawianki)

This checklist is prioritized for **Streamlit UI + Railway worker**, with an **opt-in, network-free `DEMO_MODE=1`** (JSON in `demo_db/`) and **Python 3.11**.

## How to use
- Treat this as a living checklist.
- Items are grouped by priority:
  - **P0 (must)**: prevents deploy/runtime breakages, import/path issues, data corruption.
  - **P1 (should)**: improves maintainability and safe iteration.
  - **P2 (nice)**: quality-of-life and future-proofing.

---

## P0 — Must (stability + correctness)

### P0.1 Package-safe imports everywhere
**Goal:** UI and worker run in any working directory (Streamlit Cloud, Railway, local).

**Done when:**
- No `sys.path` / `PYTHONPATH` hacks.
- All imports use `from app...` (or stdlib/third-party).
- `python -c "import app; import app.main; import app.worker.worker"` succeeds.

### P0.2 Single Data Access Layer (DAL)
**Goal:** only one place talks to Supabase / demo_store to avoid drift.

**Decision:**
- `app/data/*` is the DAL.
- UI (`app/tabs/*`) and worker/services call `app.data.*`.
- `app/core/*` should contain **pure logic** (no Supabase calls) or be removed if redundant.

**Done when:**
- No Supabase queries remain in `app/core/{bets,users,matches}.py` (moved/merged into `app/data/*`).
- Worker and services no longer import data access from `app.core.*` (except possibly a thin `app.core.db` if kept as the shared client factory).

### P0.3 DEMO_MODE is truly network-free
**Goal:** corporate laptops can run without Supabase SSL issues.

**Done when:**
- `DEMO_MODE=1` uses only local JSON in `demo_db/` and makes **no network calls**.
- DEMO_MODE behavior is centralized (single flag check).
- Docs accurately describe demo JSON (no “fixtures” language).

### P0.4 Safe persistence rules for demo_db
**Goal:** prevent demo data corruption.

**Done when:**
- Writes are atomic (tmp + replace).
- JSON schema is stable (users/matches/bets).
- Demo store functions validate minimally (e.g., required keys exist).

---

## P1 — Should (maintainability + guardrails)

### P1.1 Repo structure for collaboration
**Goal:** predictable place for docs/tests/scripts.

**Done when:**
- `docs/` exists (runbook + architecture + checklist).
- `tests/` exists (minimal pytest suite).
- Optional `scripts/` exists for local check commands.

### P1.2 Minimal tests (smoke/unit)
**Goal:** catch regressions quickly without heavy infrastructure.

**Done when:**
- `pytest -q` runs locally.
- Tests include:
  - Import/package safety
  - DEMO_MODE read/write smoke (demo_store)
  - A small pure-function unit test (e.g., filtering/scoring helper) when applicable

### P1.3 Local “CI replacement” checks
**Goal:** one command to validate before deploy/share.

**Done when:**
- A documented local command/script runs:
  - `ruff check .`
  - `pytest -q`

### P1.4 Dependency hygiene split
**Goal:** separate runtime vs dev deps.

**Done when:**
- `requirements.txt` is runtime only.
- `requirements-dev.txt` (or pyproject optional deps) includes dev tooling (pytest, ruff, etc.).
- Python version target documented (3.11).

### P1.5 Docs runbook + architecture
**Goal:** reduce tribal knowledge.

**Done when:**
- `docs/runbook.md`: local run, DEMO_MODE, env vars, troubleshooting proxy/SSL.
- `docs/architecture.md`: module responsibilities and dependency rules.

---

## P2 — Nice to have (polish)

### P2.1 Optional formatting automation
- Add `ruff format` guidance.
- Optional pre-commit hooks (not required).

### P2.2 Type hints improvements
- Expand type hints in DAL and scoring code.
- Optional mypy later (only if it helps).

### P2.3 Logging consistency
- Standardize logging format/levels across worker/services.

---

## Current known gaps (baseline)
- Duplicate Supabase access exists in both `app/core/*` and `app/data/*`.
- Some docstrings/comments still mention “fixtures” for DEMO_MODE.
- No project-owned tests folder yet (only `.venv` package tests).
