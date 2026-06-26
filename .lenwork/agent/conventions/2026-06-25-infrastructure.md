# Infrastructure Conventions

**Updated:** 2026-06-25 12:28 UTC

## Infrastructure

- Backend/persistence uses Supabase. app/core/db.py provides get_supabase() using SUPABASE_URL and SUPABASE_KEY. Secrets priority: st.secrets first, then environment/.env (via python-dotenv if installed).
