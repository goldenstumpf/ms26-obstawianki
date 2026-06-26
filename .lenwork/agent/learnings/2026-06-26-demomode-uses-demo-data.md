# Technical Learning

**Date:** 2026-06-26 09:54 UTC
**Category:** technical
**Confidence:** 5/5

## Learning

DEMO_MODE uses demo data in `demo_db/matches.json`; for UI crest rendering tests, set every match's `home_crest` and `away_crest` fields to local static URLs `/app/static/crests/home.svg` and `/app/static/crests/away.svg`.

## Context

User asked to prepare JSON and demo mode so they can test crest rendering in the UI; assistant described updating demo_db/matches.json accordingly.

## Significance

Enables consistent, offline UI testing in DEMO_MODE by ensuring deterministic crest assets across all demo matches.
