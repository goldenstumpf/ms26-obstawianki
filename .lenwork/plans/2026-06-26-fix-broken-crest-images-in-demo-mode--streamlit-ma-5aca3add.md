---
plan_id: plan-5aca3add
created: 2026-06-26T12:20:55.061841200+00:00
request: "Great, all works apart from the crests which are still showing as broken images"
status: approved
---

## Plan: Fix broken crest images in DEMO_MODE (Streamlit match row)

### Context
In DEMO_MODE you have local crest assets under `.streamlit/static/crests/*.svg`, and the URLs `/app/static/crests/home.svg` and `/app/static/crests/away.svg` open correctly in the browser. Yet the crests shown inside the match component still appear as broken images. This strongly suggests the problem is **how we build the `<img src="...">`** in the component (likely converting the URL to a filesystem path, or generating a URL the browser can’t fetch).

### Approach
Trace the crest value from DEMO_MODE data → component mapping → final HTML `<img src=...>`. Then adjust the crest rendering so, in DEMO_MODE, it uses a **browser-reachable URL** (e.g. `/app/static/crests/home.svg`) rather than a local file path like `.streamlit/static/crests/home.svg` (which the browser cannot access). Add a tiny diagnostic hook to confirm what `src` is being generated, then verify in the UI and via direct URL tests.

### Steps
1. **Confirm DEMO_MODE crest values and current mapping**
   - What: Read `demo_db/matches.json` for `home_crest/away_crest` and confirm they are `/app/static/crests/*.svg`.
   - Resources: `demo_db/matches.json`, `app/utils/components.py` (`_resolve_demo_crest_path`, `_crest_html`)
   - Output: Verified “source of truth” crest URLs in demo data and current conversion logic.

2. **Identify why the `<img>` is broken even though the URL works**
   - What: Inspect `app/utils/components.py` crest logic and determine whether, in DEMO_MODE, we are rewriting `/app/static/crests/home.svg` into a **local filesystem path** (e.g. `.streamlit/static/crests/home.svg`) and then using that as `<img src="...">` (which would break in the browser).
   - Resources: `app/utils/components.py`
   - Output: Root cause statement (expected: “we’re putting filesystem paths into `<img src>`”).

3. **Implement the correct DEMO_MODE crest strategy**
   - What (choose safest option):
     - **Option A (preferred):** In DEMO_MODE, do *not* translate `/app/static/crests/...` to a local file path for `<img>`. Keep it as the URL that already works in the browser.
     - Option B: If you truly need local-only bytes, load the SVG file and embed as `data:image/svg+xml;base64,...` (avoids any URL routing issues).
   - Resources: `app/utils/components.py` (`_crest_html`, `_resolve_demo_crest_path`)
   - Output: Crests render reliably in DEMO_MODE.

4. **Verify crest rendering in all crest usages**
   - What: Confirm crests render in:
     - team left/right name rows
     - penalty DIP display (`karne: {crest}`)
   - Resources: `app/utils/components.py`, DEMO_MODE UI
   - Output: No broken images anywhere; penalties show the winner crest when available.

5. **Regression/QA**
   - What: Run `python -m compileall -q .` and do a quick manual UI check for at least one match row and one penalty DIP case.
   - Resources: local run
   - Output: No syntax issues; UI is correct.

### Key Decisions
- Since `/app/static/crests/*.svg` opens OK in your browser, we should treat it as the authoritative, browser-reachable path in DEMO_MODE.
- Avoid using local filesystem paths in `<img src>`; they are not fetchable by the client browser.

### Expected Outcome
In DEMO_MODE, crests display correctly (no broken images) in:
- team columns (home/away)
- `karne:` DIP rendering (winner crest shown when available)

If you approve, I’ll implement Option A first (minimal change), then verify; if anything still breaks, I’ll fall back to the `data:` embedding approach.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
