---
plan_id: plan-70ee7a09
created: 2026-06-26T12:11:43.967926300+00:00
request: "Looks quite good, three things to manage now:
1. The flags are still not rendering properly,
2. We have unexpected \"0\" in match component under home and away team names,
3. DIP should not allow \"-\" empty choice.

This info box is not true:
\"Dodatkowa Informacja Pucharowa (DIP) jest wymagana tylko dla meczów pucharowych (bez remisu końcowego). Jeśli typujesz remis w 90 minut, wybierz zwycięzcę w karnych.\"

DIP is required for ANY knockout game - it needs to be 90/120 for win-lose and karne for draw have a look at the scoring component for reference if needed."
status: approved
---

## Plan: Fix crests + stray “0” + require DIP + correct help text (updated wording)

### Context
In DEMO_MODE, crests are broken again and there are stray `0` artifacts under team names. Also, DIP must be mandatory for every knockout match (no empty selection). Finally, the DIP tooltip wording must match the correct rule:
- **If bet is win/lose → choose 90 or 120**
- **If bet is draw → choose who wins penalties**

### Approach
Make small, targeted fixes in `app/utils/components.py`:
1) Remove the nested `st.columns()` inside the team columns that is likely producing the `0` artifacts.
2) In DEMO_MODE, render crests from **local files** (mapping `/app/static/crests/*.svg` → `.streamlit/static/crests/*.svg`) so it works without relying on `/app/static` routing.
3) Enforce DIP required by removing the `"-"` option and auto-selecting a valid default once both bet numbers are set.
4) Update the DIP help text to the corrected wording.

### Steps
1. **Identify exact source of the stray “0”**
   - What: Inspect the `with col1:` and `with col5:` blocks where we currently create nested `st.columns([1,9])` and `st.columns([9,1])`.
   - Resources: `app/utils/components.py`
   - Output: Confirm the exact blocks to replace.

2. **Fix crest rendering in DEMO_MODE (local only)**
   - What:
     - Add helper `_resolve_demo_crest_path(url)`:
       - if URL starts with `/app/static/crests/`, map to `.streamlit/static/crests/<file>.svg`
       - return local path if exists, else fall back to URL
     - Use `st.image(local_path, width=20)` in DEMO_MODE.
   - Resources: `app/utils/components.py`, `.streamlit/static/crests/*`
   - Output: Crests load again in DEMO_MODE.

3. **Remove stray “0” under team names**
   - What:
     - Replace nested `st.columns()` layout with a single `st.markdown(...)` row containing `<img ...> TeamName` (using resolved crest path/URL), or use `st.image` + `st.markdown` without creating extra columns inside columns.
   - Resources: `app/utils/components.py`
   - Output: No extra numeric artifacts under team names.

4. **Make DIP mandatory (no “-” option)**
   - What:
     - Remove `"-"` from selectbox options.
     - Show the selectbox only when both `home_{id}` and `away_{id}` exist.
     - If DIP missing/invalid, set default automatically:
       - non-draw bet → `"90"`
       - draw bet → `f"karne: {home_code}"`
   - Resources: `app/utils/components.py` (edit-mode DIP block), `app/tabs/submit_bets.py` (already saves `dip_{match_id}`)
   - Output: User can’t leave DIP unset for knockout matches.

5. **Correct DIP help tooltip text**
   - What: Replace help with:
     - `Jeśli typujesz zwycięstwo (win/lose), wybierz czy rozstrzygnięcie nastąpi w 90 czy w 120 minut. Jeśli typujesz remis, wybierz kto wygra w karnych.`
   - Resources: `app/utils/components.py`
   - Output: Tooltip matches your exact rule.

6. **Verification**
   - What:
     - `python -m compileall -q .`
     - DEMO_MODE manual check: crests render, no “0”, DIP can’t be empty.
   - Resources: local run in DEMO_MODE, demo knockout matches
   - Output: Confirmed UI behavior.

### Expected Outcome
- Crests render properly again in DEMO_MODE using local assets.
- No stray “0” under team names.
- DIP is always selected for knockout matches and cannot be empty.
- Tooltip text reflects the correct rule (win/lose → 90/120, draw → penalties winner).

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
