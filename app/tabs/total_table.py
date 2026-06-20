import streamlit as st
from collections import defaultdict

from core.bets import get_bets
from utils.formatters import format_username


def render_bets_table(usernames=None):

    bets = [
        b for b in get_bets(usernames)
        if b.get("points") is not None
    ]

    # grupowanie
    stats = defaultdict(lambda: {"bets": 0, "points": 0})

    for b in bets:
        u = b["username"]
        stats[u]["bets"] += 1
        stats[u]["points"] += b.get("points")

    # budowanie tabeli
    rows = []
    for i, (user, data) in enumerate(sorted(stats.items(), key=lambda x: x[1]["points"], reverse=True), start=1):
        bets_count = data["bets"]
        points = data["points"]

        rows.append({
            "N": i,
            "Gracz": format_username(user),
            "Zakłady": bets_count,
            "Punkty": f"**{points}**",
            "Pkt/Zakłady": round(points / bets_count, 4) if bets_count else 0
        })

    st.table(rows)