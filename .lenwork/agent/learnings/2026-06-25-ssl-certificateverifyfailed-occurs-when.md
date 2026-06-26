# Technical Learning

**Date:** 2026-06-25 15:43 UTC
**Category:** technical
**Confidence:** 5/5

## Learning

SSL CERTIFICATE_VERIFY_FAILED occurs when Streamlit tabs call Supabase via legacy `app/core/bets.py:get_full_bets_info()`; DEMO_MODE previously only protected `app/data/*` and did not prevent these legacy calls.

## Context

Running Streamlit app on Windows corporate laptop; app crashes with httpx/postgrest SSL certificate verify failed when loading tabs.

## Significance

When debugging demo-mode runs or corporate SSL environments, check for remaining `app/core/*` imports in UI tabs and migrate/gate them to avoid network calls and SSL errors.
