---
plan_id: plan-bf90054b
created: 2026-06-26T12:45:34.104058700+00:00
request: "Unfortunately, the imgs still showing as broken imgs - the rest of the match component is fine. The \"karne\" string should only render crest without additional code as now (now it is \"karne: {crest} {code}\" should be just \"karne: {crest}\""
status: approved
---

## Plan: Fix broken crests + make `karne:` crest-only

### Context
You’re running locally with `streamlit run streamlit_app.py` and DEMO_MODE. The component now renders:

```html
<img src="/app/static/crests/home.svg" ...>
```

…but `http://localhost:8501/app/static/crests/home.svg` “shows nothing”, so the browser can’t fetch that URL → broken images. That strongly suggests Streamlit is **not** serving static files under `/app/static/...` in your setup (likely the correct path is `/static/...`).

Separately, you want penalty display to be **crest-only**:  
`karne: {crest}` (fallback to `karne: {CODE}` only if crest missing).

### Approach
1) Make DEMO_MODE crest URLs resolve to the **actual Streamlit static URL** that works locally (very likely `/static/crests/...`), and keep a fallback strategy so it also works if `/app/static/...` is used elsewhere.

2) Remove the code from “karne” display whenever a crest is available (both bet DIP and actual DIP).

### Steps
1. **Confirm the correct static URL path in your Streamlit**
   - What: Test in browser (or via DevTools Network) these URLs:
     - `http://localhost:8501/static/crests/home.svg`
     - `http://localhost:8501/app/static/crests/home.svg`
   - Resources: your running app + browser
   - Output: Identify which path returns the SVG (200).

2. **Update crest URL normalizer to use the working path**
   - What: In `app/utils/components.py`, update `_resolve_demo_crest_url()` so it outputs:
     - `/static/crests/<file>.svg` (primary for local `streamlit run`)
     - Keep compatibility: if incoming value is `/app/static/...`, rewrite to `/static/...` (or try both)
   - Resources: `app/utils/components.py`
   - Output: `<img src="/static/crests/home.svg">` in DEMO_MODE.

3. **(Optional hardening) Switch DEMO_MODE crests to `st.image` with a local file path**
   - What: If Streamlit static serving is inconsistent across environments, we can bypass URLs entirely in DEMO_MODE:
     - map `/.../crests/x.svg` → `.streamlit/static/crests/x.svg`
     - render with `st.image(path, width=20)` (or `st.image(bytes, ...)`)
   - Resources: `app/utils/components.py`, `.streamlit/static/crests/*`
   - Output: Crests render even if static URL routing changes.

4. **Make `karne:` crest-only**
   - What: In `_format_dip_display()` and `_actual_dip_display()`:
     - If crest exists → return exactly `karne: {crest_html}` (no code appended anywhere)
     - Else → `karne: {CODE}`
   - Resources: `app/utils/components.py`
   - Output: UI shows `karne: [crest]` without trailing `ENG/GER/...`.

5. **Verification**
   - What:
     - `python -m compileall -q .`
     - Manual check: team crests render; penalty label shows crest-only; no broken imgs
   - Output: Confirmed fixed in DEMO_MODE.

### Key Decisions
- Prefer `/static/...` for local `streamlit run` if that’s what your Streamlit serves.
- Keep fallback behavior for penalty display: crest-only when available, code only if crest missing.

### Expected Outcome
- Crests render (no broken image icons) in DEMO_MODE.
- Penalty labels show **only** `karne: {crest}` (no extra code unless crest missing).

When executing, first thing I’ll do is implement Step 4 (crest-only `karne:`) since it’s deterministic, then handle the static path fix based on Step 1’s confirmed URL.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
