from datetime import datetime


def parse_kickoff(utc_string: str) -> datetime:
    """
    Parses ISO UTC string (Z or +00:00) into datetime.

    Args:
        utc_string: ISO datetime string from DB

    Returns:
        datetime (timezone-aware UTC)
    """

    return datetime.fromisoformat(utc_string.replace("Z", "+00:00"))