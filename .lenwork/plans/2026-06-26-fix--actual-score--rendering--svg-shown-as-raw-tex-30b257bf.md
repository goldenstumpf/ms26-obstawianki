---
plan_id: plan-30b257bf
created: 2026-06-26T10:57:54.560847200+00:00
request: "The actual score block is now improperly rendered. Example: \"(1 : 1  |  karne: <span style='display:in"
status: approved
---

Reading repository structure to locate where actual score block is rendered.
Searching for where the actual score block is rendered and whether unsafe_allow_html is set.
Reading the score rendering section in components.py around the lines where _scoreline_text(r) is used.
Reading the helper functions that build the scoreline/label to see how SVG/HTML is injected and whether quotes could break the HTML context.
Reading demo match data to confirm how crests are represented and reproduce the penalty case.
Reading demo matches JSON as plain text to locate a penalty match and crest URL patterns.
## Plan: Fix “actual score” rendering (SVG shown as raw text) in DEMO_MODE

### Context
In DEMO_MODE, for a penalty match (e.g., FINAL, `duration="PENALTY_SHOOTOUT"`), the “final score” line in the **middle column** (under the bet) is displaying raw `<span>...<svg ...>` text instead of rendering the crest. The bet line itself renders fine, so the issue is localized to the “final score” rendering block.

### Approach
I’ll trace exactly how the “final score under entire row” HTML is generated and rendered, then adjust the rendering strategy so SVG/HTML is reliably treated as HTML by Streamlit. The likely cause is that the inlined SVG contains double quotes/newlines and is being inserted into a context that Streamlit sanitizes/escapes or breaks due to quoting. The safest fix is to ensure the final-score block uses a rendering method that supports HTML consistently (and to keep SVG injection isolated and robust).

### Steps
1. **Locate the exact “final score” renderer and reproduce the generated string**
   - What: Inspect `app/utils/components.py` where the final score is rendered:
     ```py
     st.markdown(f""" ... ({_scoreline_text(r)}) ... """, unsafe_allow_html=True)
     ```
     Then, using your sample record (`m10`), determine what `_scoreline_text(r)` returns (it will include `karne: <span>...<svg ...>` in DEMO_MODE).
   - Resources: `app/utils/components.py` (`_scoreline_text`, `_actual_outcome_label`, `_format_penalty_display`, `_crest_img`, `_inline_svg_html_from_static_url`)
   - Output: A confirmed minimal reproduction: final-score HTML string contains raw SVG markup.

2. **Identify why Streamlit is not rendering the SVG in this specific block**
   - What: Compare the rendering contexts:
     - Bet score line uses a simple one-line `<div>` string.
     - Final score uses a multiline triple-quoted HTML block with parentheses and indentation.
     Investigate whether:
     - the triple-quoted HTML + indentation introduces text nodes/escaping,
     - the inlined SVG’s double quotes (`xmlns="..."`) are causing parsing issues inside Streamlit’s markdown/HTML pipeline,
     - Streamlit sanitization treats `<svg>` differently in markdown blocks.
   - Resources: `app/utils/components.py` and Streamlit HTML rendering behavior (based on version-agnostic constraints)
   - Output: Root cause hypothesis (escaping vs broken HTML vs sanitization) and chosen mitigation.

3. **Plan the fix: make final score use a robust HTML rendering path**
   - What (options, we’ll pick the safest):
     - **Option A (preferred):** render the final score line via `st.html(...)` if available in your Streamlit version (newer Streamlit), which is designed for raw HTML.
     - **Option B:** keep `st.markdown(..., unsafe_allow_html=True)` but change the final-score block to a single-line HTML string (no triple-quote indentation), and wrap the scoreline in a container that doesn’t get reinterpreted as markdown.
     - **Option C:** if SVG is being sanitized in markdown, fall back to `<img src="/app/static/crests/home.svg">` for the final score only (still network-free in DEMO_MODE), while keeping SVG-inlining for places where it works.
   - Resources: `app/utils/components.py`, possibly `requirements.txt` / `pyproject.toml` to confirm Streamlit version capability
   - Output: A concrete change list (what function(s) to adjust, and exactly which rendering call changes).

4. **Regression/consistency checks (no behavior drift)**
   - What: Ensure the fix does not break:
     - knockout labels (`w 90 minut`, `po dogrywce`, `karne: crest`)
     - group stage (no suffix)
     - local static crest testing (`.streamlit/static/crests/*.svg`)
     - DEMO_MODE remains network-free
   - Resources: `app/utils/components.py`, `demo_db` (you already provided a penalty example record)
   - Output: Verified expectations for the three outcomes: REGULAR/ET/PENALTIES.

5. **Verification plan**
   - What:
     - Run a quick import/compile check (`python -m compileall -q .`)
     - Manual UI check in DEMO_MODE for match `m10`:
       - The final score line under the bet should render as: `(1 : 1 | karne: [crest])` with the crest rendered, not raw SVG text.
   - Resources: local run + Streamlit UI
   - Output: Confirmed fix and no regressions.

### Key Decisions
- Keep DIP stored as code strings (no schema changes).
- Preserve DEMO_MODE network-free behavior.
- Prefer “crest rendering” whenever available; only fall back to code if crest missing.
- Choose the most reliable Streamlit HTML rendering method available for your version (likely `st.html` if supported; otherwise restructure `st.markdown` usage).

### Expected Outcome
In DEMO_MODE, the “final score under entire row” (the line under the bet in the middle column) renders the crest correctly for penalties instead of showing raw `<svg ...>` text, while keeping all previously agreed formatting rules (`w 90 minut` conditional, `po dogrywce`, and `karne: crest`).

If you want, I can also include a small “diagnostic print” plan (temporary) to log the exact generated HTML string for one match to confirm the fix targets the correct output path—but I won’t execute any changes until you approve.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
