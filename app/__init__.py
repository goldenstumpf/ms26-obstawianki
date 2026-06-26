"""Top-level package for ms26-obstawianki.

This file makes `app` a proper Python package so imports like
`from app...` work consistently across Streamlit Cloud, Railway worker, and local runs.

Project convention:
- `app.data.*` is the Data Access Layer (Supabase in production, demo_db JSON in DEMO_MODE).
- UI (`app.tabs.*`) and worker/services should call the DAL and avoid direct Supabase queries.
"""
