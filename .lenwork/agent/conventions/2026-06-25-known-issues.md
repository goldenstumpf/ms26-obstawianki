# Known-issues Conventions

**Updated:** 2026-06-25 12:28 UTC

## Known Issues

- app/services/monitor.py infinite loop monitors matches needing monitoring; helper has_matches_to_monitor() references supabase without defining it (likely missing supabase = get_supabase()), may error when run.
