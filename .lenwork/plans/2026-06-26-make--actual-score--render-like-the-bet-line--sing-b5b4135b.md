---
plan_id: plan-b5b4135b
created: 2026-06-26T11:02:54.243322300+00:00
request: "The actual score block is now improperly rendered. Example: \"(1 : 1  |  karne: <span style='display:in. Some of the previous implementations was fine, the current bet displays properly so maybe just follow the same way (keeping the separate style and inline with \"|\")"
status: approved
---

I can’t “remove the last message” from the chat history (I don’t have that capability). I also need to flag a constraint mismatch: you’re asking me to **only explore + plan** now, but we were already in **execution** (approved plan). I’ll comply with your latest instruction: **stop changes** and provide a fresh plan.

From what you describe, the fix is likely: **render the final-score line the same way as the bet line** (simple one-line `st.markdown(..., unsafe_allow_html=True)`), instead of the current multiline triple-quoted HTML block, because inline SVG markup is more likely to get escaped/treated as text in that block.

## Plan: Make “actual score” render like the bet line (single-line HTML)

### Context
In DEMO_MODE, `_scoreline_text(r)` can include inlined SVG (via `_crest_img` → `_inline_svg_html_from_static_url`). The “bet” line renders fine, but the “actual score” line (final score under the bet) displays raw `<span><svg ...>` text.

### Approach
Align the “actual score” rendering call with the bet rendering call: **one-line HTML string** passed to `st.markdown(..., unsafe_allow_html=True)`, avoiding the multiline `f""" ... """` block. Keep formatting as:  
`(1 : 1  |  karne: {crest})` and preserve the style (small, gray, margin-top).

### Steps
1. **Locate both render call sites in `app/utils/components.py`**
   - What: Identify:
     - Bet line rendering (works): `st.markdown(f"<div ...>{home_text} : {away_text}</div>", unsafe_allow_html=True)`
     - Actual score rendering (broken): current multiline `st.markdown(f""" ... ({_scoreline_text(r)}) ... """, unsafe_allow_html=True)`
   - Resources: `app/utils/components.py`
   - Output: Exact blocks to modify.

2. **Change the actual score block to a single-line HTML string**
   - What: Replace the multiline triple-quoted HTML with something analogous to the bet line, e.g.:
     - `st.markdown(f"<div style='...'>({_scoreline_text(r)})</div>", unsafe_allow_html=True)`
   - Resources: `app/utils/components.py`
   - Output: The final-score line uses the same rendering pattern as the bet line.

3. **Sanity check: ensure `_scoreline_text(r)` still returns the desired inline format**
   - What: Confirm that for penalties it returns `"{flt_home} : {flt_away}  |  karne: {crest_html}"` and not numeric pens.
   - Resources: `app/utils/components.py` (`_scoreline_text`, `_actual_outcome_label`, `_format_penalty_display`)
   - Output: Consistent output string semantics.

4. **Verification**
   - What:
     - `python -m compileall -q .`
     - Manual DEMO_MODE check with your sample match (m10 FINAL, penalties): actual score renders crest, no raw SVG text.
   - Resources: local run, DEMO_MODE
   - Output: Confirmed rendering fixed.

### Key Decisions
- Prefer the simplest Streamlit-compatible approach: **single-line HTML via `st.markdown(..., unsafe_allow_html=True)`** (same as bet line).
- Do not change DIP storage or crest logic—only the rendering container.

### Expected Outcome
The “actual score” line under the bet renders exactly like:
`(1 : 1  |  karne: [crest])`
with the crest rendered (not raw SVG text), while keeping the same styling and inline `|` separator.

If you confirm you want this approach, the next execution step is a small edit in `app/utils/components.py` limited to that final-score `st.markdown` block.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
