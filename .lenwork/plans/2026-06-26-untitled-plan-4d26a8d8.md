---
plan_id: plan-4d26a8d8
created: 2026-06-26T11:56:55.168260800+00:00
request: "We need to rebuild the match component then (I believe everything else is fine):
1. In edit mode, when the match is in knockout stage, we need to have a dropdown with label \"DIP\" and information hover \"Dodatkowa Informacja Pucharowa (DIP) jest wymagana...\" short info on what and when is required. The dropdown should allow to choose \"90\" (displayed \"w 90 minut\") or \"120\" (displayed as \"po dogrywce\") if the bet is win/lose, if it is draw (bet_home == bet_away), then we need to dropdown f\"karne: {home_code}\" or away code.
2. In the read mode, the bet needs to display the main bet and DIP (if it exists, thus for knockout games) underneath (with the same colour and styling, just slightly smaller and small margin) - if the DIP is duration type it should just show \"w 90 minut\" or \"po dogrywce\", if \"karne: \" add home/away flag accordingly.
3. In the read mode, the actual score should also incorporate actual DIP inline after \"|\" sign - using the same content rules as the bet.
4. The flags are not displayed properly in the current component"
status: approved
---

Got it — we’ll reuse these **exact semantics** in the match component so UI and scoring stay aligned:

- **Bet DIP parsing**: if `dip` starts with `karne` → extract the team code after `karne:` (or `karne `).
- **Actual penalty winner**: use `pens_home/pens_away` first, fallback to `flt_home/flt_away`.

In the rebuild plan, that means:

1) In **view mode bet DIP rendering**:
- if `dip == "90"` → `w 90 minut`
- if `dip == "120"` → `po dogrywce`
- if `_parse_penalty_dip(dip)` returns a code:
  - match it against `home_code/away_code`
  - render `karne: <crest>` for the matching side (fallback to `karne: CODE` if crest missing)

2) In **view mode actual score DIP rendering**:
- if `duration == "PENALTY_SHOOTOUT"`:
  - compute winner via `_penalty_winner_code(match)`
  - render `karne: <winner crest>` (fallback to code)
- if `duration == "EXTRA_TIME"`: `po dogrywce`
- if `duration == "REGULAR"` and knockout: `w 90 minut`

When we implement, I’ll either:
- copy these two functions into `app/utils/components.py` (UI-layer versions), or
- import them from `app/services/score_bets.py` (I prefer copying small pure helpers to avoid coupling UI to services).

Next step (once you approve execution in BUILD mode): implement these helpers + DIP dropdown + crest rendering fixes in `app/utils/components.py`.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
