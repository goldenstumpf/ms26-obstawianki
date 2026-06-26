from collections import defaultdict

import streamlit as st

from app.data.full_bets_info import get_full_bets_info
from app.utils.components import render_match_row
from app.utils.formatters import format_username

# =========================================================
# HELPERS
# =========================================================

def build_user_totals(records):
    table = defaultdict(lambda: {"points": 0.0})

    for r in records:
        user = r["username"]
        table[user]["points"] += float(r.get("points") or 0)

    return dict(table)


def build_closed_totals(records):
    table = defaultdict(lambda: {"points": 0.0})

    for r in records:
        if r.get("status") != "closed":
            continue

        user = r["username"]
        table[user]["points"] += float(r.get("points") or 0)

    return dict(table)


def ranking(table):
    return sorted(table.items(), key=lambda x: x[1]["points"], reverse=True)


def build_rank_map(ranking_list):
    return {user: i + 1 for i, (user, _) in enumerate(ranking_list)}


# =========================================================
# ROW RENDERER
# =========================================================

def render_row(rank, user, bet_text, match_points, total_points, delta):

    st.markdown(
        f"""
        <div style="
            display:flex;
            font-size:14px;
            padding:3px 0;
            align-items:center;
        ">

            <div style="flex:0 0 35px;">
                {rank}
            </div>

            <div style="flex:2;font-weight:500;overflow:hidden;white-space:nowrap;">
                {format_username(user)}
            </div>

            <div style="flex:2;text-align:center;">
                {bet_text}
            </div>

            <div style="flex:1;text-align:center;font-weight:600;">
                {match_points:.2f}
            </div>

            <div style="flex:1;text-align:center;font-weight:700;">
                {total_points:.2f}
            </div>

            <div style="flex:1;text-align:center;">
                {delta}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MAIN TAB
# =========================================================

def render_live_tab():

    st.title("🔴 Centrum LIVE")

    records = get_full_bets_info()

    # =====================================================
    # LIVE MATCHES (MULTI)
    # =====================================================
    live_matches = [r for r in records if r.get("status") == "live"]

    st.subheader("🔴 Na żywo")

    if live_matches:
        for m in live_matches:
            render_match_row(m, mode="view")
    else:
        st.info("Brak trwających meczów")

    st.divider()

    # =====================================================
    # LAST 3 CLOSED MATCHES
    # =====================================================
    closed_matches = [
        r for r in records if r.get("status") == "closed"
    ]

    closed_matches = sorted(
        closed_matches,
        key=lambda r: r.get("utc_date") or "",
        reverse=True
    )[:3]

    st.subheader("⚫ Ostatnie mecze")

    if closed_matches:
        for m in closed_matches:
            render_match_row(m, mode="view")
    else:
        st.info("Brak zakończonych meczów")

    st.divider()

    # =====================================================
    # TABLE LOGIC
    # =====================================================

    closed_table = build_closed_totals(records)
    live_table = build_user_totals(records)

    closed_ranking = ranking(closed_table)
    live_ranking = ranking(live_table)

    closed_rank_map = build_rank_map(closed_ranking)

    # =====================================================
    # HEADER
    # =====================================================
    st.markdown(
        """
        <div style="
            display:flex;
            font-weight:600;
            font-size:13px;
            opacity:0.7;
            margin-bottom:6px;
        ">
            <div style="width:35px">#</div>
            <div style="flex:2">Gracz</div>
            <div style="flex:2;text-align:center;">Zakłady LIVE</div>
            <div style="flex:1;text-align:center;">Pkt LIVE</div>
            <div style="flex:1;text-align:center;">Suma</div>
            <div style="flex:1;text-align:center;">+/-</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # ROWS (MULTI LIVE SAFE)
    # =====================================================
    for i, (user, stats) in enumerate(live_ranking, start=1):

        live_pos = i
        closed_pos = closed_rank_map.get(user)

        # MULTI LIVE MATCHES
        user_live_bets = [
            r for r in records
            if r["username"] == user and r.get("status") == "live"
        ]

        match_points = sum(float(r.get("points") or 0) for r in user_live_bets)

        bet_text = " | ".join(
            f"{r.get('home_bet')}:{r.get('away_bet')}"
            for r in user_live_bets
            if r.get("home_bet") is not None
        ) or "-"

        # DELTA
        if closed_pos is None:
            delta = "🆕"
        else:
            diff = closed_pos - live_pos
            if diff > 0:
                delta = f"🟢 +{diff}"
            elif diff < 0:
                delta = f"🔴 {diff}"
            else:
                delta = "⚪ 0"

        render_row(
            rank=live_pos,
            user=user,
            bet_text=bet_text,
            match_points=match_points,
            total_points=stats["points"],
            delta=delta
        )