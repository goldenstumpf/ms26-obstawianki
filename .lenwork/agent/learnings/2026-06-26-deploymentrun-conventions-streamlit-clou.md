# Technical Learning

**Date:** 2026-06-26 07:04 UTC
**Category:** technical
**Confidence:** 4/5

## Learning

Deployment/run conventions: Streamlit Cloud entrypoint is streamlit_app.py at repo root calling app.main.run; Railway worker runs via python -m app.worker.worker.

## Context

Review of repo deploy targets and README run commands.

## Significance

Helps maintain consistent packaging/imports and correct deployment documentation going forward.
