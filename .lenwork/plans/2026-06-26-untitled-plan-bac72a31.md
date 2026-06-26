---
plan_id: plan-bac72a31
created: 2026-06-26T09:00:48.684140300+00:00
request: "Please adjust demo db to be able to test the new streamlit UI for betting and reporting"
status: approved
---

I can do that, but per the system instructions I need to **explore + plan first (no changes yet)**.

### What “adjust demo db” should cover (so UI testing is meaningful)
To properly test the **new Streamlit betting UI + reporting** with DIP, demo data should include:

1) **Matches across stages**
- Some `GROUP_STAGE` matches (no DIP required)
- Some knockout matches (`LAST_16`, `QUARTER_FINALS`, etc.) where DIP **is required**

2) **Finished + upcoming + live mix**
- At least a few `FINISHED` matches with:
  - `duration=REGULAR`
  - `duration=EXTRA_TIME`
  - `duration=PENALTY_SHOOTOUT` with `pens_home/pens_away`
- A few upcoming matches so “Submit bets” has bettable rows.

3) **Bets for at least 2 users**
- For knockout matches:
  - at least one **draw bet** with `dip="karne: XXX"`
  - at least one **non-draw bet** with `dip="90"` and another with `dip="120"`
- Ensure some bets have points and some don’t, so report sorting/filters are testable.

### Clarification I need (1 question, then I’ll execute)
When you say “to be able to test betting and reporting”, do you want demo_db to ship with **pre-filled bets** for the demo users (so reports show something immediately), or do you prefer starting mostly blank and entering bets manually?

Reply with one of:
- **A)** “pre-filled bets for alice/bob/charlie”
- **B)** “mostly blank, I’ll enter bets manually”

Once you answer, I’ll:
- inspect `demo_db/matches.json` + current `demo_db/bets.json`
- patch them to include knockout + finished penalty/ET cases and DIP examples
- run a quick DEMO_MODE smoke to confirm the UI behaves (DIP selector shows up / report displays DIP + penalties).

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
