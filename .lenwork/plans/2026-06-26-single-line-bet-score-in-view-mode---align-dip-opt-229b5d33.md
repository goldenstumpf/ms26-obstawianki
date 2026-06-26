---
plan_id: plan-229b5d33
created: 2026-06-26T10:33:50.806917800+00:00
request: "Crests are now displayed fine but we still need to have the bet score in one line \"2 : 1 | po dogrywce\" and not in two. I have also manually changed dip_options in _is_knockout_stage in edit mode of components.py - ensure this is aligned across the code."
status: approved
---

## Plan: Single-line bet score in view mode + align DIP options/storage across code

### Context
Crests now render correctly. Remaining UI issue: in **view/report mode** the bet score is shown on one line (`2 : 1`) and DIP on a second grey line underneath; you want this combined into **one line** like `2 : 1 | po dogrywce` (bet + bet DIP). The **actual result** line underneath (in parentheses) is already correct and should stay as-is.

You also manually changed `dip_options` in **edit mode** for knockout non-draw bets to `["w 90 minut", "po dogrywce"]`. We need to ensure this is aligned across the codebase—especially with **stored DIP values** used by scoring logic.

### Approach
1) Update **view mode** rendering in `render_match_row` so the bet score line includes the formatted DIP suffix inline (knockout only).  
2) Normalize DIP option values so edit-mode choices are consistent with:
- what gets **stored** (`dip` value)
- what gets **displayed** (`_format_dip`)
- what scoring expects (per scoring rules: stored values are `"90"` / `"120"` or `"karne: CODE"`)

To keep compatibility, we’ll treat `"w 90 minut"` and `"po dogrywce"` as **display labels**, but ensure the stored values remain `"90"` / `"120"` (unless you explicitly want to migrate stored data).

### Steps
1. **Inspect current `render_match_row` view mode bet score rendering**
   - What: Identify the exact block that prints:
     - bet line: `<div>home_text : away_text</div>`
     - then DIP line underneath (grey)
   - Resources: `app/utils/components.py` (view-mode middle column)
   - Output: Precise edit points and desired combined HTML string.

2. **Implement single-line bet score + DIP in view mode**
   - What:
     - In `_is_knockout_stage(r)` and when `r.get("dip")` exists, compute `dip_txt = _format_dip(r.get("dip"), r)`
     - Render bet line as: `"{home_text} : {away_text}  |  {dip_txt}"` (or similar spacing)
     - Remove (or gate off) the second “DIP under bet” line to avoid duplication
   - Resources: `app/utils/components.py`, `_format_dip`
   - Output: View-mode bet display becomes one line: `2 : 1 | po dogrywce` (and penalties show `karne: <crest>` inline).

3. **Align edit-mode DIP options with stored values**
   - What:
     - Your manual change set non-draw options to `["w 90 minut", "po dogrywce"]`.
     - Scoring rules (and `_format_dip`) are built around stored `"90"` / `"120"` for non-draw bets.
     - Plan: change edit-mode options back to stored values `["90", "120"]` but display them as “w 90 minut” / “po dogrywce” via `format_func`, **or** accept both inputs by adding mapping logic.
   - Resources:
     - `app/utils/components.py` (edit-mode DIP selectbox)
     - `app/services/score_bets.py` (to confirm what it expects)
     - `app/data/bets.py` / `app/data/demo_store.py` (storage)
   - Output: Users see Polish labels, but DB/demo store keeps `"90"`/`"120"` (no scoring regression).

4. **Scan for other places that display bet + DIP**
   - What: Check `app/tabs/live_center.py`, `app/tabs/_experimental_dashboard.py`, reports, etc. for similar bet rendering patterns.
   - Resources: repo grep results (targets found in your project already)
   - Output: Confirm single-line formatting is consistent everywhere you want it, or keep it limited to `render_match_row` if that’s your preference.

5. **Verification**
   - What:
     - `python -m compileall -q .`
     - Quick run in DEMO_MODE:
       - knockout match with DIP `120` → bet line shows `| po dogrywce`
       - knockout draw bet DIP `karne: HOME_CODE` → bet line shows `| karne: <crest>`
       - group stage bet → remains `2 : 1` (no suffix)
   - Output: Confirm UI exactly matches: bet inline, actual score underneath unchanged, and scoring still works.

### Key Decisions
- **Do we keep stored DIP values as `"90"/"120"`?**  
  I recommend yes (matches your scoring rules and avoids data migration). The UI can still show “w 90 minut / po dogrywce”.

- **Scope**: apply single-line bet formatting only in `render_match_row` view mode unless you confirm you want it also in dashboards/live tab.

### Expected Outcome
- In view/report mode, the **bet** shows on one line:  
  `2 : 1 | po dogrywce` (or `| karne: <crest>` for penalties)
- The **actual result** remains underneath in parentheses (already working).
- Edit-mode DIP options are aligned so the UI labels are Polish, but stored values remain compatible with scoring everywhere.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
