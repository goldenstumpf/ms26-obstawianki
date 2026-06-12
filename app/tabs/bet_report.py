import streamlit as st
from core.bets import get_user_bets_report
from utils.formatters import format_score
from utils import pl_translations as pl
from utils.ui import render_bet_native

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
    
    live = sorted(live, key=lambda b: b.get("match_number"))
    pending = sorted(pending, key=lambda b: b.get("match_number"))
    closed = sorted(closed, key=lambda b: b.get("match_number"), reverse=True)

    col1, col2, col3 = st.columns(3)

    # ================= PENDING =================
    with col1:
        st.subheader("🗓️ WKRÓTCE")

        for bet in pending:
            render_bet_native(bet, pl)

    # ================= LIVE =================
    with col2:
        st.subheader("🔴 NA ŻYWO")

        live_sum = sum(bet.get("points") or 0 for bet in live)

        if len(live) > 0:
            st.markdown(f"**Punkty: +{live_sum}**")


        for bet in live:
            render_bet_native(bet, pl)

    # ================= CLOSED =================
    with col3:
        st.subheader("🟢 ZAKOŃCZONE")

        closed_sum = sum(bet.get("points") or 0 for bet in closed)
        st.markdown(f"**Punkty: {closed_sum}**")


        for bet in closed:
            render_bet_native(bet, pl)