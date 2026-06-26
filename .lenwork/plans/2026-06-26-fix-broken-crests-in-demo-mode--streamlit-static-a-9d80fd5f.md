---
plan_id: plan-9d80fd5f
created: 2026-06-26T12:29:32.859950700+00:00
request: "Great, all works apart from the crests which are still showing as broken images"
status: approved
---

## Plan: Fix broken crests in DEMO_MODE (Streamlit static assets)

### Context
In DEMO_MODE your `<img>` tags currently use `src=".streamlit\static\crests\home.svg"` (a filesystem-ish Windows path with backslashes). Browsers won’t reliably load that as an image URL inside HTML, so you get broken images even though the file exists.

You already have the correct “public URL” convention: **`.streamlit/static/...` is served by Streamlit as `/app/static/...`** (your earlier rule: `.streamlit/static/crests/*.svg` → `/app/static/crests/*.svg`).

### Approach
Stop rewriting DEMO crest URLs to local filesystem paths for `<img src=...>`. Instead, always give the browser a **web path** it can request:

- Prefer `/app/static/crests/<name>.svg` in DEMO_MODE (network-free; served locally by Streamlit)
- Normalize slashes (`\` → `/`) and ensure we never emit `.streamlit\...` into `<img src>`

### Steps
1. **Audit current crest URL flow**
   - What: Inspect `app/utils/components.py` helpers `_resolve_demo_crest_path()` and `_crest_html()`, and confirm where the `.streamlit\static\...` string is introduced.
   - Resources: `app/utils/components.py`
   - Output: Identified exact transformation producing broken `src`.

2. **Change DEMO_MODE crest rewriting to a browser-loadable URL**
   - What:
     - Update `_crest_html()` so that in DEMO_MODE:
       - if crest_url starts with `/app/static/crests/` → keep it (best case)
       - if crest_url looks like a local path under `.streamlit/static/...` → convert to `/app/static/...`
       - never return backslashes in `src` (replace `\` with `/`)
     - Optionally remove/stop using `_resolve_demo_crest_path()` for HTML `<img>` (file existence checks can stay, but **not** via `src`).
   - Resources: `app/utils/components.py`
   - Output: `<img src="/app/static/crests/home.svg" ...>` in DEMO_MODE.

3. **Quick verification**
   - What:
     - Run `python -m compileall -q .`
     - Run Streamlit in DEMO_MODE and confirm:
       - Team crests render
       - Penalty “karne:” winner crest renders
       - No broken images in view/edit modes
   - Resources: local run, DevTools Network (optional)
   - Output: Crests render reliably in DEMO_MODE, still network-free.

### Key Decisions
- For HTML `<img>`, **use URL paths**, not filesystem paths.
- DEMO_MODE stays network-free because `/app/static/...` is served locally by Streamlit from `.streamlit/static/...`.

### Expected Outcome
In DEMO_MODE, crests show correctly everywhere (team rows + “karne:” winner), with `src` values like:

- `/app/static/crests/home.svg`
- `/app/static/crests/away.svg`

and no `.streamlit\static\...` paths emitted into HTML.

If you approve, I’ll implement this only in `app/utils/components.py` (helper-level fix), then do the compile check and you can re-run the UI.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
