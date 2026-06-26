# Technical Learning

**Date:** 2026-06-26 12:03 UTC
**Category:** technical
**Confidence:** 5/5

## Learning

Match component requirements: in knockout stage edit mode show DIP selectbox; options depend on bet (win/lose -> stored values "90"/"120"; draw -> stored values "karne: {home_code}" or "karne: {away_code}"); read mode shows bet DIP underneath; actual score shows actual DIP inline after "|"; crests should render reliably (prefer st.image).

## Context

Reviewing conversation about implementing DIP semantics and crest rendering in app/utils/components.py.

## Significance

Captures the project-specific DIP data model and rendering rules so future changes keep UI, stored values, and scoring aligned.
