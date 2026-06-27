"""Data access layer (DAL).

This package contains small, reusable functions that talk to Supabase (production)
or the local JSON demo database in `demo_db/` (DEMO_MODE=1).

UI code should prefer importing from `app.data.*` instead of calling Supabase
queries directly.
"""
