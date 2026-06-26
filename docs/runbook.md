# Runbook

## Local run (Windows / PowerShell)

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# UI
streamlit run streamlit_app.py

# Worker (Railway-like)
python -m app.worker.worker
```

## DEMO_MODE (network-free local development)

Use DEMO_MODE when Supabase calls fail on corporate laptops (proxy / SSL inspection), e.g.:
`SSL: CERTIFICATE_VERIFY_FAILED`.

```powershell
$env:DEMO_MODE = "1"
streamlit run streamlit_app.py
```

DEMO_MODE behavior:
- No calls to Supabase.
- Data is stored locally as JSON under `demo_db/`:
  - `demo_db/users.json`
  - `demo_db/matches.json`
  - `demo_db/bets.json`

To return to production behavior:

```powershell
Remove-Item Env:DEMO_MODE -ErrorAction SilentlyContinue
```

## Required environment variables

### Production (Supabase)
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `FOOTBALL_API_KEY`

### DEMO_MODE
- `SUPABASE_URL` / `SUPABASE_KEY` not required.
- `FOOTBALL_API_KEY` only needed if you run code that calls the external football API.

## Deploy notes

### Streamlit Cloud
- **Main file path**: `streamlit_app.py`
- Configure secrets: `SUPABASE_URL`, `SUPABASE_KEY`, `FOOTBALL_API_KEY`

### Railway (worker)
- Start command: `python -m app.worker.worker`
- Configure environment variables as above.

## Local quality checks (no hosted CI)

```powershell
# Lint
python -m ruff check .

# Tests
python -m pytest -q

# Or run the convenience script
.\scripts\check.ps1
```
