import streamlit as st

import core.i18n as pl
from utils.time import format_datetime, parse_kickoff


def render_match_row(r: dict, mode: str = "edit"):
    """
    mode:
    - "edit" → number inputs (betting)
    - "view" → read-only (report)
    """

    match_id = str(r["match_id"])

    home_pl = pl.country(r["home_team"])
    away_pl = pl.country(r["away_team"])

    stage_pl = pl.stage(r.get("stage", ""))
    group_pl = pl.group(r.get("group_name", ""))

    date_pl = format_datetime(parse_kickoff(r["utc_date"]))

    is_bet = r.get("home_bet") is not None and r.get("away_bet") is not None

    # -------------------------
    # HEADER STATUS
    # -------------------------
    if mode == "edit":
        if is_bet:
            st.success("✔ Obstawione")
        else:
            st.info("✏️ Do obstawienia")

    else:
        if r.get("status") in {"IN_PLAY", "PAUSED", "EXTRA_TIME", "PENALTY_SHOOTOUT"}:
            st.markdown("🔴 LIVE")
        elif r.get("points") is not None:
            st.markdown("⚫ Zakończony")
        else:
            st.markdown("🟡 Nadchodzący")

    # -------------------------
    # META
    # -------------------------
    st.caption(
        f"MECZ #{r['match_number']} | "
        f"{group_pl or stage_pl} | "
        f"{date_pl}"
    )

    # -------------------------
    # ROW LAYOUT
    # -------------------------
    col1, col2, col3, col4, col5 = st.columns([5, 1.2, 0.5, 1.2, 5])

    with col1:
        st.markdown(
            f"<div style='text-align:right'>"
            f"{home_pl} <img src='{r['home_crest']}' width='20'>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # -------------------------
    # EDIT MODE
    # -------------------------
    if mode == "edit":

        home_key = f"home_{match_id}"
        away_key = f"away_{match_id}"

        if home_key not in st.session_state:
            st.session_state[home_key] = r.get("home_bet")

        if away_key not in st.session_state:
            st.session_state[away_key] = r.get("away_bet")

        with col2:
            st.number_input(
                "home_goals",
                min_value=0,
                step=1,
                key=home_key,
                label_visibility="collapsed",
            )

        with col3:
            st.markdown(
                f"<div style='text-align:center'>"
                f":"
                f"</div>",
            unsafe_allow_html=True,
        )

        with col4:
            st.number_input(
                "away_goals",
                min_value=0,
                step=1,
                key=away_key,
                label_visibility="collapsed",
            )

    # -------------------------
    # VIEW MODE
    # -------------------------
    else:
        with col2:
            st.markdown(
                f"<div style='text-align:right'>"
                f"{r.get('home_bet', '-') }"
                f"</div>",
            unsafe_allow_html=True,
        )
            
        with col3:
            st.markdown(
                f"<div style='text-align:center'>"
                f":"
                f"</div>",
            unsafe_allow_html=True,
        )

        with col4:
            st.markdown(
                f"<div style='text-align:left'>"
                f"{r.get('away_bet', '-') }"
                f"</div>",
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            f"<div style='text-align:left'>"
            f"<img src='{r['away_crest']}' width='20'> {away_pl}"
            f"</div>",
            unsafe_allow_html=True,
        )

    # -------------------------
    # FOOTER (only report mode)
    # -------------------------
    if mode == "view" and r.get("points") is not None:
        st.caption(f"🏆 {r['points']} pkt")

    st.divider()