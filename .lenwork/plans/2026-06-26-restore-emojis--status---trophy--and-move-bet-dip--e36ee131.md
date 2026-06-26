---
plan_id: plan-e36ee131
created: 2026-06-26T10:44:27.262278500+00:00
request: "The yellow/red/black dots now render as \"??\" (was fine before) as well as the cup icon next to points. Also, the inline is fine now but you can see that it does not fit one line, maybe let's go back to rendering it underneath the main score (the bet DIP) but use slightly smaller font and the same colour as the main bet so it is not mistaken for the actual score"
status: approved
---

## Plan: Restore emojis (status + trophy) and move bet DIP back under bet score (tight spacing, same color)

### Context
Two regressions are visible in the UI:

1) Several emojis (status dots + ✏️/✔ + 🏆) are now rendered as `??` in Streamlit output. This is not a Streamlit bug; it’s because the source strings in `app/utils/components.py` were inadvertently changed to contain `??` instead of emojis (likely via encoding/replace during previous PowerShell edits).

2) The bet DIP appended inline (`2 : 1 | po dogrywce`) wraps on narrow layout. You want to revert to the previous layout: **bet score on one line**, and **bet DIP underneath**, but styled as part of the bet (same color, slightly smaller) with **very tight spacing**, while keeping the **actual score** line underneath with **slightly more spacing** (and still grey).

You confirmed:
- Use **emojis** (restore original icons).
- Bet DIP under bet score: **same color**, **slightly smaller**, **very tight spacing**.

### Approach
- Fix the emoji regression by restoring the original emoji strings in `components.py`.
- Update view-mode rendering so bet score is one line, and bet DIP is a second line beneath it (but *not grey*). This avoids wrapping while still visually associating DIP with the bet.
- Keep the “actual score” line as-is but adjust spacing to make it clearly separate (more space than bet DIP line).

### Steps
1. **Locate and restore emoji strings**
   - What: In `app/utils/components.py`, restore:
     - Edit-mode header: `✔ Obstawione`, `✏️ Do obstawienia`
     - View-mode status: `🔴 Na żywo`, `⚫ Zakończony`, `🟡 Nadchodzący`
     - Footer points: `🏆 {points} pkt`
   - Resources: `app/utils/components.py` (header status section + footer section)
   - Output: UI shows proper emojis instead of `??`.

2. **Change view/report bet display to two lines (score + bet DIP)**
   - What: In `render_match_row(..., mode="view")`:
     - Keep main bet score line: `home_text : away_text`
     - If knockout + dip present:
       - render bet DIP on a new line under it using `_format_dip(r.get("dip"), r)`
       - style: same color as bet score (default), slightly smaller font, tight spacing
     - Remove the inline `| dip` suffix currently appended.
   - Resources: `app/utils/components.py` view-mode middle column block
   - Output: Bet DIP no longer wraps; it’s under the bet score and visually grouped with it.

3. **Adjust spacing between bet DIP line and actual score line**
   - What:
     - Bet DIP line: keep tight (e.g., `margin-top:-6px`)
     - Actual score (grey parentheses): slightly more spacing than DIP line (e.g., change `margin-top:-8px` to a less negative / positive value)
   - Resources: `app/utils/components.py` final-score-under-row markdown block
   - Output: Bet DIP isn’t mistaken for actual score; actual score is visually separated.

4. **Verify build + quick UI checks**
   - What:
     - `python -m compileall -q .`
     - Run Streamlit and confirm:
       - status shows correct emoji dots
       - points show 🏆
       - bet score line stays clean, bet DIP below is readable, actual score is clearly separate
   - Resources: local run, DEMO_MODE and non-demo if available
   - Output: No regressions; layout matches screenshot expectations.

### Key Decisions
- Stick with **emojis** (per your preference) rather than CSS dots/icons.
- DIP back to “under bet” display to avoid wrapping, but **not grey** (so it doesn’t look like the actual score).

### Expected Outcome
- Status indicators and trophy render correctly again (🔴/🟡/⚫, 🏆, ✔, ✏️).
- Bet display in view mode:
  - line 1: `2 : 1`
  - line 2 (tight, same color, slightly smaller): `po dogrywce` / `w 90 minut` / `karne: <crest>`
- Actual score remains in parentheses underneath, grey, with a bit more separation so it’s not confused with bet DIP.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
