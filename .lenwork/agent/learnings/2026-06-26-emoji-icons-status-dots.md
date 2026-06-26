# Technical Learning

**Date:** 2026-06-26 10:49 UTC
**Category:** technical
**Confidence:** 5/5

## Learning

Emoji icons (status dots, trophy, check/pencil) showing as '??' were caused by source strings being replaced and/or the file `app/utils/components.py` being saved in a non-UTF-8 encoding (cp1250). Fix by restoring emoji literals and ensuring the file is UTF-8.

## Context

Investigating UI regression where emojis rendered as '??' in Streamlit and restoring proper rendering.

## Significance

Helps quickly diagnose future emoji/rendering regressions: check for accidental string replacement and file encoding; enforce UTF-8 to preserve emoji.
