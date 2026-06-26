# Conventions Conventions

**Updated:** 2026-06-25 15:43 UTC

## Conventions

- `DEMO_MODE=1` should make the app fully network-free by routing all UI data access through `app/data/*` functions (e.g., `list_matches`, `list_bets`) that fall back to fixtures.
