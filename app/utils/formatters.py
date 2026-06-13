def format_score(bet):
    h = bet.get("flt_home")
    a = bet.get("flt_away")

    if h is None or a is None:
        return "-"

    return f"{h}:{a}"

def display_username(username: str):
    parts = username.split("-")

    formatted = []

    for part in parts:
        if len(part) == 1:
            formatted.append(part.upper() + ".")
        else:
            formatted.append(part.capitalize())

    return " ".join(formatted)