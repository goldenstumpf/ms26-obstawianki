# Technical Learning

**Date:** 2026-06-26 10:10 UTC
**Category:** technical
**Confidence:** 4/5

## Learning

Project uses DEMO_MODE with crest URLs like /app/static/crests/*.svg that map to files in .streamlit/static/crests/. Central crest rendering is in app/utils/components.py via a helper _crest_img(), which should be used everywhere (including match row headers and DIP karne display) so the DEMO_MODE SVG-inlining fix applies consistently.

## Context

Implementing end-to-end crest rendering fix and ensuring headers use _crest_img() instead of hardcoded <img> tags.

## Significance

Prevents future regressions where parts of the UI bypass the central crest renderer and reintroduce broken icons; clarifies local static file mapping in DEMO_MODE.
