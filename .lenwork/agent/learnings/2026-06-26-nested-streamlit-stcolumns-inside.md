# Solution Learning

**Date:** 2026-06-26 12:16 UTC
**Category:** solution
**Confidence:** 3/5

## Learning

Nested Streamlit st.columns inside existing columns can cause stray rendering artifacts (e.g., unexpected "0" under team names); using a single HTML flex row or avoiding nested columns can fix it.

## Context

Diagnosing unexpected "0" artifacts in the match component under home/away team names.

## Significance

Provides a reusable fix pattern for Streamlit layout issues that may reappear in this project.
