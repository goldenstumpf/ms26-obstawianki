import streamlit as st
from core.bets import get_user_bets_report
from utils.formatters import format_score
from utils import pl_translations as pl

def render_bet_report():

    username = st.session_state["user"]
    bets = get_user_bets_report(username)

    live = []
    pending = []
    closed = []

    for bet in bets:
        if bet["status"] == "live":
            live.append(bet)
        elif bet["status"] == "closed":
            closed.append(bet)
        else:
            pending.append(bet)

    col1, col2, col3 = st.columns(3)

    # ================= PENDING =================
    with col1:
        st.subheader("🗓️ WKRÓTCE")

        for bet in pending:
            st.write(
                f"{pl.country(bet['home_team'])} {bet['home']} - {bet['away']} {pl.country(bet['away_team'])}"
            )

    # ================= LIVE =================
    with col2:
        st.subheader("🔴 NA ŻYWO")

        live_sum = sum(bet.get("points") or 0 for bet in live)
        st.metric("Punkty na żywo: +", live_sum)

        for bet in live:
            st.write(
                f"{pl.country(bet['home_team'])} {bet['home']} - {bet['away']} {pl.country(bet['away_team'])} "
                f"| {format_score(bet)} | {bet.get('points', 0)}"
            )

    # ================= CLOSED =================
    with col3:
        st.subheader("🟢 ZAKOŃCZONE")

        closed_sum = sum(bet.get("points") or 0 for bet in closed)
        st.metric("Punkty zdobyte: ", closed_sum)

        for bet in closed:
            st.write(
                f"{pl.country(bet['home_team'])} {bet['home']} - {bet['away']} {pl.country(bet['away_team'])} "
                f"| {format_score(bet)} | {bet.get('points', 0)}"
            )