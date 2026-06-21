import streamlit as st

from core.bets import get_full_bets_info
from utils.components import render_match_row


LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT",
}


def render_bet_report():
    st.title("📊 Mój raport")
    st.caption("Wszystkie Twoje zakłady i mecze w jednym miejscu")
    st.divider()

    username = st.session_state["user"]

    # -------------------------
    # DATA LOAD
    # -------------------------
    records = [
        r for r in get_full_bets_info()
        if r["username"] == username
    ]

    if not records:
        st.info("Brak danych do wyświetlenia.")
        return

    # -------------------------
    # OPTIONAL FILTERS
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        show_live = st.checkbox("🔴 Tylko live", False)

    with col2:
        show_bets = st.checkbox("🟢 Tylko obstawione", False)

    with col3:
        show_pending = st.checkbox("🟡 Tylko bez betu", False)

    def _filter(r: dict) -> bool:
        if show_live and r.get("status") not in LIVE_STATUSES:
            return False

        if show_bets and (r.get("home_bet") is None or r.get("away_bet") is None):
            return False

        if show_pending and (r.get("home_bet") is not None):
            return False

        return True

    records = [r for r in records if _filter(r)]

    # -------------------------
    # SORTING (logic + readability)
    # -------------------------
    def _sort_key(r: dict):
        # live first
        if r.get("status") in LIVE_STATUSES:
            return 0

        # not bet yet
        if r.get("home_bet") is None:
            return 1

        # bet placed
        return 2

    records.sort(key=_sort_key)

    # -------------------------
    # SUMMARY (lightweight, no stats engine yet)
    # -------------------------
    total = len(records)
    bet_count = sum(1 for r in records if r.get("home_bet") is not None)
    live_count = sum(1 for r in records if r.get("status") in LIVE_STATUSES)

    col1, col2, col3 = st.columns(3)
    col1.metric("Mecze", total)
    col2.metric("Obstawione", bet_count)
    col3.metric("Live", live_count)

    st.divider()

    # -------------------------
    # RENDER
    # -------------------------
    for r in records:
        render_match_row(r, mode="view")