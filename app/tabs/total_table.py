from collections import defaultdict

import streamlit as st

from app.data.bets import list_bets
from app.utils.formatters import format_username


def render_bets_table(usernames=None):
    all_bets = list_bets(username=None)

    if usernames is None:
        bets = [b for b in all_bets if b.get("points") is not None]
    else:
        username_set = set(usernames)
        bets = [
            b
            for b in all_bets
            if b.get("username") in username_set and b.get("points") is not None
        ]

    stats = defaultdict(lambda: {"bets": 0, "points": 0})

    for b in bets:
        u = b["username"]
        stats[u]["bets"] += 1
        stats[u]["points"] += b.get("points")

    rows = []
    for i, (user, data) in enumerate(
        sorted(stats.items(), key=lambda x: x[1]["points"], reverse=True), start=1
    ):
        bets_count = data["bets"]
        points = data["points"]

        rows.append(
            {
                "N": i,
                "Gracz": format_username(user),
                "Zakłady": bets_count,
                "Punkty": f"**{points}**",
                "Pkt/Zakłady": round(points / bets_count, 4) if bets_count else 0,
            }
        )

    st.table(rows)
