# Workflow Learning

**Date:** 2026-06-26 07:30 UTC
**Category:** workflow
**Confidence:** 3/5

## Learning

Local quality gate pattern: use ruff + pytest, with dev deps separated (requirements-dev.txt) and an optional scripts/check.ps1 runner; Windows execution policy may block running .ps1, so document running underlying commands directly.

## Context

Setting up local CI-equivalent checks for the repo without hosted CI

## Significance

Avoids friction on Windows machines and keeps checks reproducible without CI.
