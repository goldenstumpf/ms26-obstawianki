import streamlit as st

from core.bets import save_bets, get_full_bets_info
from core.matches import get_bettable_matches
import core.i18n as pl
from utils.time import format_datetime, parse_kickoff


def render_submit_bets():
    st.title("Złóż zakłady")
    st.caption("Typuj wyniki meczów z nadchodzących 72 godzin.")
    st.divider()

    username = st.session_state["user"]

    # =========================
    # DATA (single source)
    # =========================
    records = get_full_bets_info()

    # filtrowanie tylko meczów możliwych do obstawienia
    bettable_matches = get_bettable_matches(
        [r for r in records if r["username"] == username]
    )
    bettable_ids = {m["match_id"] for m in bettable_matches}

    records = [
        r for r in records
        if r["username"] == username
        and r["match_id"] in bettable_ids
    ]

    bets = {}

    # =========================
    # UI
    # =========================
    for r in records:
        match_id = str(r["match_id"])

        home_key = f"home_{match_id}"
        away_key = f"away_{match_id}"

        # init state (existing bet or None)
        st.session_state.setdefault(home_key, r.get("home_bet"))
        st.session_state.setdefault(away_key, r.get("away_bet"))

        is_bet = r.get("home_bet") is not None and r.get("away_bet") is not None

        home_pl = pl.country(r["home_team"])
        away_pl = pl.country(r["away_team"])

        stage_pl = pl.stage(r.get("stage", ""))
        group_pl = pl.group(r.get("group_name", ""))

        date_pl = format_datetime(parse_kickoff(r["utc_date"]))

        if is_bet:
            st.success("✔ Obstawione")
        else:
            st.info("✏️ Do obstawienia")

        st.caption(
            f"MECZ #{r['match_number']} | {group_pl or stage_pl} | {date_pl}"
        )

        col1, col2, col3, col4, col5 = st.columns([5, 1.2, 0.5, 1.2, 5])

        with col1:
            st.markdown(
                f"<div style='text-align:right'>{home_pl} <img src='{r['home_crest']}' width='20'></div>",
                unsafe_allow_html=True
            )

        with col2:
            home_goals = st.number_input(
                "Gole H",
                min_value=0,
                step=1,
                key=home_key,
                label_visibility="collapsed"
            )

        with col3:
            st.markdown(
                "<div style='text-align:center;padding-top:8px'>:</div>",
                unsafe_allow_html=True
            )

        with col4:
            away_goals = st.number_input(
                "Gole A",
                min_value=0,
                step=1,
                key=away_key,
                label_visibility="collapsed"
            )

        with col5:
            st.markdown(
                f"<div style='text-align:left'><img src='{r['away_crest']}' width='20'> {away_pl}</div>",
                unsafe_allow_html=True
            )

        bets[match_id] = {
            "home_bet": home_goals,
            "away_bet": away_goals
        }

        st.divider()

    # =========================
    # SAVE
    # =========================
    if st.button("💾 Zapisz wszystkie typy"):

        result = save_bets(
            username=username,
            bets=bets
        )

        st.success(f"✔ Zapisano zmian: {result['changed']}")

        if result["skipped"] > 0:
            st.warning(
                f"Pominięto: {result['skipped']} (brak zakładu / nieprawidłowe dane)"
            )