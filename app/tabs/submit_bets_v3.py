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
    # DATA
    # =========================
    records = [
        r for r in get_full_bets_info()
        if r["username"] == username
    ]

    bettable_matches = get_bettable_matches(records)
    bettable_ids = {m["match_id"] for m in bettable_matches}

    records = [
        r for r in records
        if r["match_id"] in bettable_ids
    ]

    # =========================
    # SPLIT
    # =========================
    not_bet = [
        r for r in records
        if r.get("home_bet") is None and r.get("away_bet") is None
    ]

    bet = [
        r for r in records
        if r.get("home_bet") is not None and r.get("away_bet") is not None
    ]

    # zachowanie kolejności jak wcześniej
    # (zakładam, że records już ma sensowny order)

    def render_match_block(match_list, title, success_flag=False):
        if not match_list:
            return {}

        st.subheader(title)

        bets_out = {}

        for r in match_list:

            match_id = str(r["match_id"])

            home_key = f"home_{match_id}"
            away_key = f"away_{match_id}"

            if home_key not in st.session_state:
                st.session_state[home_key] = r.get("home_bet")

            if away_key not in st.session_state:
                st.session_state[away_key] = r.get("away_bet")

            is_bet = r.get("home_bet") is not None

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
                st.markdown("<div style='text-align:center;padding-top:8px'>:</div>", unsafe_allow_html=True)

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

            bets_out[match_id] = {
                "home_bet": home_goals,
                "away_bet": away_goals
            }

            st.divider()

        if st.button(f"💾 Zapisz wszystkie typy ({title})"):
            result = save_bets(username=username, bets=bets_out)

            st.success(f"✔ Zapisano zmian: {result['changed']}")

            if result["skipped"] > 0:
                st.warning(f"Pominięto: {result['skipped']}")

        return bets_out

    # =========================
    # UI SECTIONS
    # =========================

    render_match_block(not_bet, "🟡 Nieobstawione")
    st.divider()
    render_match_block(bet, "🟢 Obstawione")