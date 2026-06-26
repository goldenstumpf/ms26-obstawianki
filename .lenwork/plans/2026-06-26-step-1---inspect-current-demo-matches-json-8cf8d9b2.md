---
plan_id: plan-8cf8d9b2
created: 2026-06-26T09:51:26.946438100+00:00
request: "Prepare the json and demo mode so I can test on demo mode in UI"
status: approved
---

Plan (no execution yet) to prepare DEMO_MODE JSON so your UI shows the local SVG crests everywhere:

## Step 1 — Inspect current demo matches JSON
**What this does:** confirm the shape of `demo_db/matches.json` (list vs dict, field names used).  
**Resources:** `demo_db/matches.json`  
**Expected outcome:** know exactly how to update `home_crest` / `away_crest` for every match.

## Step 2 — Update ALL matches to use your two local static crest URLs
**What this does:** sets the same two crests across all demo matches so every row renders them.
- `home_crest` → `/app/static/crests/home.svg`
- `away_crest` → `/app/static/crests/away.svg`
(Optionally also set `*_crest` if any matches are missing the key.)  
**Resources:** `demo_db/matches.json`  
**Expected outcome:** every demo match has deterministic crest URLs that Streamlit can serve locally.

## Step 3 — Quick validation (no network)
**What this does:** ensures the JSON stays valid and DEMO_MODE still runs without Supabase.
- Validate JSON parses
- (Optional) run `python -m compileall -q .`  
**Resources:** python runtime, demo_db JSON  
**Expected outcome:** no syntax/JSON errors introduced.

## Step 4 — Deep QA
**What this does:** re-open the modified JSON and verify:
- all matches got updated
- no fields got accidentally removed
- URLs are exactly correct  
**Expected outcome:** confidence that DEMO_MODE UI will render the crests reliably.

When you say “go”, I’ll execute these steps by editing `demo_db/matches.json` accordingly.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
