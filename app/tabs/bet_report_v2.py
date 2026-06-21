import streamlit as st

from core.bets import get_full_bets_info
from core.matches import get_bettable_matches
import core.i18n as pl
from utils.time import format_datetime, parse_kickoff


LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT",
}


def _status_badge(r: dict) -> str:
    if r["status"] in LIVE_STATUSES:
        return "🔴 LIVE"

    if r.get("points") is not None:
        return "⚫ FINISHED"

    if r.get("home_bet") is None:
        return "🟡 NO BET"

    return "🟢 BET"


def render_my_report():

    st.title("📊 Mój raport")
    st.caption("Wszystkie Twoje zakłady i mecze w jednym miejscu")
    st.divider()

    username = st.session_state["user"]

    records = [
        r for r in get_full_bets_info()
        if r["username"] == username
    ]

    # -------------------------
    # FILTERS (simple but useful)
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        show_only_live = st.checkbox("Tylko live", False)

    with col2:
        show_only_bets = st.checkbox("Tylko obstawione", False)

    with col3:
        show_only_pending = st.checkbox("Tylko bez betu", False)

    # -------------------------
    # APPLY FILTERS
    # -------------------------
    def match_filter(r):
        if show_only_live and r["status"] not in LIVE_STATUSES:
            return False

        if show_only_bets and r.get("home_bet") is None:
            return False

        if show_only_pending and r.get("home_bet") is not None:
            return False

        return True

    records = [r for r in records if match_filter(r)]

    # -------------------------
    # SORT (stable, intuitive)
    # live → upcoming → finished
    # -------------------------
    def sort_key(r):
        if r["status"] in LIVE_STATUSES:
            return 0
        if r.get("home_bet") is None:
            return 1
        return 2

    records.sort(key=sort_key)

    # -------------------------
    # RENDER
    # -------------------------
    for r in records:

        match_id = r["match_id"]

        home_pl = pl.country(r["home_team"])
        away_pl = pl.country(r["away_team"])

        date_pl = format_datetime(parse_kickoff(r["utc_date"]))

        status = _status_badge(r)

        home_bet = r.get("home_bet")
        away_bet = r.get("away_bet")

        points = r.get("points")

        # -------------------------
        # HEADER LINE
        # -------------------------
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <b>MECZ #{r['match_number']}</b> | {date_pl}
                </div>
                <div>{status}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------
        # MAIN ROW (flags inline style like submit_bets)
        # -------------------------
        col1, col2, col3 = st.columns([5, 2, 5])

        with col1:
            st.markdown(
                (
                    f"<div style='text-align:right'>"
                    f"{home_pl} "
                    f"<img src='{r['home_crest']}' width='20'>"
                    f"</div>"
                ),
                unsafe_allow_html=True,
            )

        with col2:
            if home_bet is None:
                st.markdown("— : —")
            else:
                st.markdown(
                    (
                        f"<div style='text-align:center'>"
                        f"**{home_bet} : {away_bet}**"
                        f"</div>"
                     ),
                    unsafe_allow_html=True,
                )

        with col3:
            st.markdown(
                (
                    f"<div style='text-align:left'>"
                    f"<img src='{r['away_crest']}' width='20'> "
                    f"{away_pl}"
                    f"</div>"
                ),
                unsafe_allow_html=True,
            )

        # -------------------------
        # FOOTER INFO
        # -------------------------
        footer = []

        if points is not None:
            footer.append(f"🏆 {points} pkt")

        if r.get("home_bet") is None:
            footer.append("Brak zakładu")

        if footer:
            st.caption(" | ".join(footer))

        st.divider()