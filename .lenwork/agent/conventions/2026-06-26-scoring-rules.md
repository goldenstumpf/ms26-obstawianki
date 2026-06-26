# Scoring-rules Conventions

**Updated:** 2026-06-26 08:50 UTC

## Scoring & Rules

- Scoring v2 requirements: base points 4 exact score, 2 goal diff, 1 result (home/away/draw; draw result counts only in GROUP_STAGE). Near-miss bonus +0.5 if abs(home_bet-home_goals)+abs(away_bet-away_goals)==1. Knockout requires DIP per bet: if non-draw bet -> DIP '90' or '120'; if draw bet -> DIP 'karne: {home_code}' or 'karne: {away_code}'. Duration DIP bonus +1 if base>=1 and (DIP=='90' and duration==REGULAR) or (DIP=='120' and duration==EXTRA_TIME). Penalty DIP bonus +1 if DIP 'karne: XXX' matches shootout winner, even if base==0. Score reconciliation: for exact score/goal diff/duration DIP use extra-time score fallback to full-time (if no ET); duration DIP points are additional. For result/penalty DIP use penalties result fallback to extra time then full time; penalty DIP complementary not additional.
