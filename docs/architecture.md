# Architecture

This repo contains:
- **Streamlit UI** (entrypoint: `streamlit_app.py` → `app.main.run()`)
- **Worker** (entrypoint: `python -m app.worker.worker`) which runs scheduled fetch + scoring loops

## Package/import rule
- All imports should be package-safe: `from app...`
- Avoid `sys.path` hacks.

## Module responsibilities

### `app/tabs/*` (UI)
- Streamlit pages/screens.
- Should not contain database/network details.
- Should call the DAL (`app.data.*`).

### `app/data/*` (DAL)
- Data Access Layer.
- The only place that should talk to:
  - Supabase (production)
  - `demo_db/` JSON via `demo_store` (DEMO_MODE)

### `app/services/*` (background jobs)
- Fetching matches, scoring bets, monitoring gate.
- Should use `app.data.*` for all persistence.

### `app/worker/*` (runtime loop)
- Scheduling and orchestration of services.

### `app/core/*` (domain logic)
- Shared pure logic (formatting rules, calculations, helpers).
- Should not talk to Supabase directly.

## DEMO_MODE
- Enabled via `DEMO_MODE=1` environment variable.
- Intended for local development when Supabase connectivity is unavailable.
- Must remain network-free.
