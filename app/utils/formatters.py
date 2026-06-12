def format_score(bet):
    h = bet.get("flt_home")
    a = bet.get("flt_away")

    if h is None or a is None:
        return "-"

    return f"{h}:{a}"