from datetime import datetime, timedelta, timezone
from core.db import get_supabase
from typing import TypedDict, Optional
from utils.time import parse_kickoff

# =========================
# MODELS
# =========================

class Match(TypedDict):
    match_id: str
    match_number: int
    utc_date: str

    home_team: str
    away_team: str

    status: str
    duration: Optional[int]

    flt_home: Optional[int]
    flt_away: Optional[int]

    ext_home: Optional[int]
    ext_away: Optional[int]

    pens_home: Optional[int]
    pens_away: Optional[int]

    stage: str
    group_name: str

    home_crest: str
    away_crest: str

    home_code: str
    away_code: str
    
    minute: Optional[int]

# =========================
# READ
# =========================

def get_matches() -> list[Match]:
    """
    Returns all matches ordered by kickoff time.

    Returns:
        list[Match]
    """

    res = (
        get_supabase()
        .table("matches")
        .select("*")
        .order("utc_date")
        .execute()
    )

    return res.data or []


def get_bettable_matches(
    matches: list[Match],
    hours: int = 72
) -> list[Match]:
    """
    Returns matches available for betting.

    A match is bettable if:
    - has both teams set
    - has valid kickoff time
    - is within betting window (now → now + hours)
    """

    now = datetime.now(timezone.utc)
    limit = now + timedelta(hours=hours)

    result: list[Match] = []

    for m in matches:
        if not m.get("home_team") or not m.get("away_team"):
            continue

        utc_date = m.get("utc_date")
        if not utc_date:
            continue

        match_time = parse_kickoff(utc_date)

        if now <= match_time <= limit:
            result.append(m)

    return result