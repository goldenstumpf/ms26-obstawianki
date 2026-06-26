# Technical Learning

**Date:** 2026-06-26 12:03 UTC
**Category:** technical
**Confidence:** 4/5

## Learning

DIP parsing/semantics: bet dip value "90" => REGULAR, "120" => EXTRA_TIME, and strings starting with "karne" include a team code after "karne:" (or "karne ") to indicate penalty winner selection for draw bets. Actual penalty winner should be derived from pens_home/pens_away, falling back to flt_home/flt_away.

## Context

Aligning UI and scoring semantics for knockout DIP in match component.

## Significance

Prevents mismatches between how DIP is stored/displayed and how scoring interprets it.
