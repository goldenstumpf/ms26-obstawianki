def format_score(home: int | None, away: int | None) -> str:
    if home is None or away is None:
        return "-"
    return f"{home}:{away}"


def format_username(username: str) -> str:
    parts = username.split("-")

    return " ".join(
        p.upper() + "." if len(p) == 1 else p.capitalize()
        for p in parts
    )