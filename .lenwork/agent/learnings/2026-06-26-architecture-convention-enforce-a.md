# Convention Learning

**Date:** 2026-06-26 07:30 UTC
**Category:** convention
**Confidence:** 4/5

## Learning

Architecture convention: enforce a single data-access layer—only app.data.* should talk to Supabase/demo_store; UI/worker/services should not query Supabase directly (avoid duplication between app/core/* and app/data/*).

## Context

Repo restructuring and boundary cleanup during professionalization

## Significance

Guides future refactors and code reviews to prevent DAL drift and duplicated database logic.
