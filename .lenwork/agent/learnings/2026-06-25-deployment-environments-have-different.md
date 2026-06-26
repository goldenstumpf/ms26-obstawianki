# Technical Learning

**Date:** 2026-06-25 12:30 UTC
**Category:** technical
**Confidence:** 5/5

## Learning

Deployment environments have different import roots: Streamlit Cloud runs app/main.py such that `app/` behaves like the import root (imports like `from tabs...`, `from core...` work), while Railway worker runs from repo root expecting `from app...` absolute package imports.

## Context

Diagnosing inconsistent Python imports between Streamlit UI and Railway worker deployments.

## Significance

Helps prevent future import errors by aligning packaging/import strategy across environments and informing where to set PYTHONPATH or adjust entrypoints.
