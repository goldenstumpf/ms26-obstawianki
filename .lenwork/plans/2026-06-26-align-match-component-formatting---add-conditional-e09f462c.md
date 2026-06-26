---
plan_id: plan-e09f462c
created: 2026-06-26T10:15:03.469092600+00:00
request: "Ok, let's revisit what we planned to do before:
Actually let's align the two formattings exactly (in match component):
2 : 1 | po dogrywce (in line)
Underneath as is now, the actual score, in the actual score also add \"w 90 minut\" but only if extra time would be possible (ie. when this is not a group stage/ DIP is present)
Additionally, if \"karne\" is used, show karne: {crest} and not the code"
status: approved
---

## Plan: Align match component formatting + add conditional “w 90 minut” + show crest for “karne” (also in DEMO_MODE)

### Context
In `app/utils/components.py` (match component), you want the **inline** and **underneath** score formatting aligned:

- Inline (existing “actual score” line):  
  `2 : 1 | po dogrywce` (same line)

- Underneath (currently `({scoreline})`): keep it, but **also add** `| w 90 minut` **only for knockout matches** when the match ended in regular time.

Additionally, whenever penalties are involved, the label must be:
- `karne: {crest}` (not the code) — and you want this **also in DEMO_MODE**.

You confirmed the condition for “extra time possible” is simply: **knockout stage** (`_is_knockout_stage(r)`).

### Approach
I will:
1) make outcome-label generation consistent for both inline and underneath scorelines,
2) extend `_actual_outcome_label()` so it can return `w 90 minut` for knockout regular-time finishes,
3) remove the DEMO_MODE exception that forces `karne: CODE`, so “karne” always uses crest when available,
4) ensure both places use the same helper function(s) so they cannot drift.

### Steps
1. **Update `_actual_outcome_label(r)` to cover all knockout outcomes**
   - What:
     - If `duration == "EXTRA_TIME"` → `"po dogrywce"`
     - If `duration == "PENALTY_SHOOTOUT"` → `"karne: <crest>"` (winner crest when available; no code fallback unless crest missing)
     - If `duration == "REGULAR"` **and** `_is_knockout_stage(r)` → `"w 90 minut"`
     - Else (group stage regular time) → `None`
   - Resources: `app/utils/components.py` (`_actual_outcome_label`, `_penalty_winner_code`, `_format_penalty_display`, `_crest_img`)
   - Output: A single source of truth for the “| …” suffix.

2. **Adjust `_format_penalty_display(...)` to always prefer crest**
   - What: Remove the current “DEMO_MODE shows code” behavior. New behavior:
     - if `crest_url` exists → `karne: <crest>`
     - else → `karne: <code>` (last resort)
   - Resources: `app/utils/components.py`
   - Output: “karne” displays with crest consistently (demo + prod) as long as crest is present.

3. **Align the two score renderings in `render_match_row`**
   - What:
     - The inline “final score under entire row” will keep using `_scoreline_text(r)` but `_scoreline_text` will now include:
       - `| w 90 minut` for knockout regular finishes
       - `| po dogrywce` for ET
       - `| karne: <crest>` for penalties
     - The “actual score” (inline in the row) remains as-is (your current “underneath actual score” line) but we’ll ensure it uses the same suffix logic (i.e., also uses `_actual_outcome_label(r)`).
   - Resources: `app/utils/components.py` (`render_match_row`, `_scoreline_text`)
   - Output: Both places show identical semantics; group stage stays clean (`2 : 1` only).

4. **Verification**
   - What:
     - `python -m compileall -q .`
     - Manual DEMO_MODE UI check with at least:
       - one GROUP_STAGE finished match → shows `(2 : 1)` (no suffix)
       - one knockout REGULAR finished match → shows `| w 90 minut`
       - one knockout EXTRA_TIME match → shows `| po dogrywce`
       - one knockout PENALTY_SHOOTOUT match with crests → shows `karne: <crest>`
   - Resources: DEMO_MODE data in `demo_db/matches.json`, local run
   - Output: Confirmed formatting in UI.

### Key Decisions
- “Extra time possible” = `_is_knockout_stage(r)` (per your answer).
- “Karne” shows **crest even in DEMO_MODE**; code only if crest is missing.

### Expected Outcome
In the match component:
- Group stage finished: `(2 : 1)` only
- Knockout regular finish: `(2 : 1 | w 90 minut)`
- Knockout extra time: `(2 : 1 | po dogrywce)`
- Knockout penalties: `(2 : 1 | karne: <crest>)`

When you approve, I’ll implement these changes strictly inside `app/utils/components.py` and run the compile check.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
