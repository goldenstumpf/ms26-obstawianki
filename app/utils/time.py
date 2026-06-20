from datetime import datetime
from zoneinfo import ZoneInfo


def parse_kickoff(utc_string: str) -> datetime:
    return datetime.fromisoformat(utc_string.replace("Z", "+00:00"))


def to_poland_time(dt: datetime) -> datetime:
    return dt.astimezone(ZoneInfo("Europe/Warsaw"))

def format_datetime(dt: datetime, short: bool = False) -> str:
    dt = to_poland_time(dt)

    if short:
        return dt.strftime("%d.%m %H:%M")

    return dt.strftime("%d.%m.%Y %H:%M")