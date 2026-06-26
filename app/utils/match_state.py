"""Match state classification shared across UI and tabs.

This module exists to avoid circular imports between UI components and tabs.

Semantics must remain aligned with the bet report:
- LIVE: status == 'live' (legacy/UI marker) OR status in LIVE_STATUSES (match API caps)
- FINISHED: final score is present (flt_home/flt_away) AND match is not live
- UPCOMING: otherwise
"""

from __future__ import annotations

from typing import Literal


LIVE_STATUSES: set[str] = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT",
    "LIVE",
}


MatchState = Literal["LIVE", "FINISHED", "UPCOMING"]


def classify_match_state(r: dict) -> MatchState:
    """Classify a merged match record into LIVE / FINISHED / UPCOMING.

    IMPORTANT: In merged records, bet.status (e.g. 'pending'/'closed') can overwrite
    match.status (e.g. 'LIVE'/'FINISHED') because merge is {**match, **bet}.

    We therefore treat:
    - match live statuses (caps) as live
    - 'live' (lowercase) as a legacy/UI live marker

    Also note: flt_* may appear "on the go"; a match is FINISHED only if it is NOT live.
    """

    status = r.get("status")

    is_live = (status == "live") or (status in LIVE_STATUSES)

    has_result = r.get("flt_home") is not None and r.get("flt_away") is not None
    is_finished = (not is_live) and has_result

    if is_live:
        return "LIVE"
    if is_finished:
        return "FINISHED"
    return "UPCOMING"
