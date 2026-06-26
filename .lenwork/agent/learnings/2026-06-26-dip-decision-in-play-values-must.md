# Technical Learning

**Date:** 2026-06-26 10:37 UTC
**Category:** technical
**Confidence:** 5/5

## Learning

DIP (decision-in-play) values must remain stored as codes compatible with scoring logic: non-draw knockout DIP uses "90"/"120"; draw uses "karne: {TEAM_CODE}". Polish labels ("w 90 minut", "po dogrywce") should be display-only via formatting/format_func, with normalization if legacy labels appear.

## Context

Aligning dip_options in _is_knockout_stage/edit-mode selectbox with scoring/storage and rendering bet line with DIP inline.

## Significance

Prevents scoring regressions and keeps UI labels user-friendly while maintaining consistent stored values across the codebase.
