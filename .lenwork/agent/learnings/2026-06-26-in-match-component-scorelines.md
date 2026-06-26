# Convention Learning

**Date:** 2026-06-26 10:29 UTC
**Category:** convention
**Confidence:** 5/5

## Learning

In match component scorelines, append outcome suffixes in Polish with ` | ` delimiter: `po dogrywce` for extra time, `w 90 minut` only when extra time would be possible (knockout stage), and `karne: {crest}` for penalties (never show just the code if crest is available, including in DEMO_MODE).

## Context

Align match component formatting and implement conditional `w 90 minut` and crest-based `karne` display.

## Significance

Ensures future UI/formatting changes preserve the exact scoreline conventions and conditional logic for knockout vs group-stage matches, and consistent crest rendering for penalties.
