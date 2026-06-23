import streamlit as st
from collections import defaultdict

from core.bets import get_full_bets_info
from utils.formatters import format_username
from utils.components import render_match_row


# =========================================================
# TABLE HELPERS
# =========================================================

def build_user_totals(records):
    """
    Total points per user (all matches)
    """
    table = defaultdict(lambda: {"points": 0.0})

    for r in records:
        user = r["username"]
        table[user]["points"] += float(r.get("points") or 0)

    return dict(table)


def build_closed_totals(records):
    """
    Ranking baseline (only closed)
    """
    table = defaultdict(lambda: {"points": 0.0})

    for r in records:
        if r.get("status") != "closed":
            continue

        user = r["username"]
        table[user]["points"] += float(r.get("points") or 0)

    return dict(table)


def build_rank_map(ranking):
    return {user: i + 1 for i, (user, _) in enumerate(ranking)}


def ranking(table):
    return sorted(table.items(), key=lambda x: x[1]["points"], reverse=True)


# =========================================================
# TABLE ROW (SAFE STREAMLIT - NO BROKEN HTML)
# =========================================================

def render_row(rank, user, bet, match_points, total_points, delta):

    home_bet = bet.get("home_bet")
    away_bet = bet.get("away_bet")

    bet_text = (
        f"{home_bet}:{away_bet}"
        if home_bet is not None and away_bet is not None
        else "-"
    )
    st.markdown(
            f"""
            <div style="
                display:flex;
                font-size:14px;
                padding:2px 0;
                align-items:center;
            ">
                <div style="width:35px">{rank}</div>
                <div style="flex:2;font-weight:500">{format_username(user)}</div>
                <div style="flex:1;text-align:center;">{bet_text}</div>
                <div style="flex:1;text-align:center;font-weight:600;">{match_points}</div>
                <div style="flex:1;text-align:center;">{total_points}</div>
                <div style="flex:1;text-align:center;">{delta}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# LIVE TAB
# =========================================================

def render_live_tab():

    st.title("🔴 LIVE")

    records = get_full_bets_info()

    # -------------------------
    # TOP: MATCH
    # -------------------------
    live_match = next((r for r in records if r.get("status") == "live"), None)

    if live_match:
        render_match_row(live_match, mode="view")
    else:
        st.info("Brak meczu LIVE")

    st.divider()

    # -------------------------
    # TABLE PREP
    # -------------------------
    closed_table = build_closed_totals(records)
    live_table = build_user_totals(records)

    closed_rank = build_rank_map(ranking(closed_table))
    live_ranking = ranking(live_table)

    # -------------------------
    # HEADER
    # -------------------------
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
            <div style="flex:1;text-align:center;">Typ</div>
            <div style="flex:1;text-align:center;">Mecz</div>
            <div style="flex:1;text-align:center;">Suma</div>
            <div style="flex:1;text-align:center;">+/-</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # ROWS
    # -------------------------
    for i, (user, stats) in enumerate(live_ranking, start=1):

        # znajdź bet do LIVE meczu
        user_match = next(
            (r for r in records
             if r["username"] == user and r.get("status") == "live"),
            {}
        )

        match_points = float(user_match.get("points") or 0)

        live_pos = i
        closed_pos = closed_rank.get(user)

        if closed_pos is None:
            delta = "🆕"
        else:
            diff = closed_pos - live_pos
            delta = f"🔼 {diff}" if diff > 0 else f"🔽 {abs(diff)}" if diff < 0 else "⏺️"

        render_row(
            rank=live_pos,
            user=user,
            bet=user_match,
            match_points=match_points,
            total_points=stats["points"],
            delta=delta
        )