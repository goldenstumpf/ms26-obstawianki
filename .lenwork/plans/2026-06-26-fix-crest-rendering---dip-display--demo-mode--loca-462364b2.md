---
plan_id: plan-462364b2
created: 2026-06-26T10:00:23.700838900+00:00
request: "The imgs are not rendering properly and the dropdown and reporting is not using the crests but codes"
status: approved
---

## Plan: Fix crest rendering + DIP display (DEMO_MODE, local SVGs)

### Context
In DEMO_MODE you pointed match crests to `/app/static/crests/*.svg`, but in the UI they show as a **broken icon**. Separately, the **DIP dropdown** shows codes (expected, because it’s built from strings), but for **read/report mode** you want `karne:` to show the **winner crest** (not the code). You confirmed you’re OK keeping **codes in the dropdown**, as long as read-mode DIP shows crests.

### Approach
I’ll tackle this in two tracks: (1) make crest images render reliably in Streamlit by switching away from raw HTML `<img src="...">` for SVGs (or by adding a safe fallback), and (2) ensure read-mode DIP uses the existing `_format_dip(dip, r)` crest rendering path everywhere it’s displayed. We’ll keep dropdown storage as codes (`karne: BRA`) but format display in view/report mode.

### Steps
1. **Reproduce & locate broken crest rendering**
   - What: Identify all places that render crests using `<img src='...'>` and confirm which ones are used in your DEMO_MODE screens.
   - Resources: `app/utils/components.py`, tabs that display matches (e.g. report tab uses `render_match_row`).
   - Output: List of exact rendering points to change.

2. **Make crest rendering reliable for local SVGs**
   - What: Replace HTML `<img>` usage with a Streamlit-safe approach:
     - Prefer `st.image(...)` where possible, or
     - Inline SVG content (read file + `st.markdown(svg, unsafe_allow_html=True)`), or
     - Convert SVGs to PNG for demo mode (optional fallback) and point demo JSON to PNG.
   - Resources: `app/utils/components.py` (central rendering), possibly `.streamlit/static/crests/*`.
   - Output: Crests render in UI (no broken icons) in DEMO_MODE.

3. **Ensure read/report DIP uses crest formatting for “karne”**
   - What: Verify every view/report mode path that displays DIP calls `_format_dip(dip, r)` (with record context). We already fixed the “DIP under bet” path in `render_match_row`; we’ll check other renderers (tables/dashboards).
   - Resources: `app/utils/components.py`, any other tab rendering DIP directly.
   - Output: In read/report mode, penalty DIP shows `karne:` + crest (outside DEMO_MODE rules if applicable), while dropdown remains codes.

4. **Verification**
   - What: Run local checks and a quick manual UI sanity checklist:
     - `DEMO_MODE=1 streamlit run streamlit_app.py`
     - Verify crests render in match header and read-mode “karne” DIP displays correctly.
   - Resources: local run + minimal compile/import checks.
   - Output: You can test UI in DEMO_MODE with working crests and correct DIP display.

### Key Decisions
- Keep **codes in the DIP dropdown** (you approved).
- Show **crests only in read/report mode** DIP for `karne`.
- Prefer a rendering method that doesn’t rely on the browser successfully loading SVG via `<img src="/app/static/...svg">`, since that’s what’s breaking.

### Expected Outcome
- No more broken crest icons in DEMO_MODE UI.
- DIP dropdown continues to store/show codes for selection.
- In view/report mode, `karne:` DIP displays with the winner crest (as intended).

If you approve, I’ll execute starting with Step 1 (locate all crest rendering points and adjust the central renderer in `app/utils/components.py`).

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
