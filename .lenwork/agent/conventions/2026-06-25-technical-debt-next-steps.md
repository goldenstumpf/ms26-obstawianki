# Technical-debt-next-steps Conventions

**Updated:** 2026-06-25 14:28 UTC

## Technical Debt / Next Steps

- Next step: migrate remaining tabs (bet_report, table, live_center) off get_full_bets_info() onto DAL patterns (targeted fetch + small in-memory joins); then add app/analytics with pure functions for new analytics tabs (team leaderboards, best predictor per team, what-if standings, rules tab).
