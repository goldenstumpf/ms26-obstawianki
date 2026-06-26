# Ui-rendering Conventions

**Updated:** 2026-06-26 10:37 UTC

## UI Rendering

- In app/utils/components.py render_match_row (view/report mode), bet score should include DIP suffix inline for knockout matches when dip exists, using `_format_dip(r.get('dip'), r)`, e.g., `2 : 1 | po dogrywce`; avoid rendering DIP on a separate grey line.
- In `app/utils/components.py` (Streamlit components), render bet in view/report mode as two lines: main bet score on first line; bet DIP on second line styled as same color as bet, slightly smaller (e.g., 13px) with tight margin (e.g., -6px). Keep actual score line in grey with a bit more spacing (e.g., margin-top -2px) so it’s visually distinct.
