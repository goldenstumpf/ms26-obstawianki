# Data-model-api Conventions

**Updated:** 2026-06-26 08:50 UTC

## Data Model / API

- API context: stage enum [FINAL, THIRD_PLACE, SEMI_FINALS, QUARTER_FINALS, LAST_16, LAST_32, LAST_64, ROUND_4, GROUP_STAGE]; duration enum [REGULAR, EXTRA_TIME, PENALTY_SHOOTOUT]. Need to store more than full-time-only: persist penalties and treat 'final score before penalties' (pre-pen) as key scoreline for scoring. UI match component must expand in edit/read modes to show FT/ET/penalties and collect DIP accordingly.
