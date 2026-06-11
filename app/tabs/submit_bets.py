import streamlit as st
from core.matches import get_matches, defined_matches, get_upcoming_matches
from core.bets import save_user_bets
from utils import pl_translations as pl


def render_submit_bets():
    
    st.set_page_config(
        page_title="MŚ 2026 - Typowanie",
        layout="centered"
    )

    st.title("Zielone Zakłady 2026")

    matches = get_matches()

    # Filtrowanie meczów
    matches_to_display = get_upcoming_matches(defined_matches(matches))    

    bets = {}

    for match in matches_to_display:

        home_pl = pl.country(match["homeTeam"]["name"])
        away_pl = pl.country(match["awayTeam"]["name"])

        stage_pl = pl.stage(match.get("stage", ""))
        group_pl = pl.group(match.get("group", ""))

        date_pl = pl.format_kickoff(match["utcDate"])

        st.caption(
            f"MECZ #{match['matchNumber']} | {group_pl or stage_pl} | {date_pl}"
        )

        col1, col2, col3, col4, col5 = st.columns(
            [5, 1.2, 0.5, 1.2, 5]
        )

        with col1:
            st.markdown(
                f"<div style='text-align:right'>{home_pl}</div>",
                unsafe_allow_html=True
            )

        with col2:
            home_goals = st.number_input(
                "Gole H",
                min_value=0,
                step=1,
                key=f"home_{match['id']}",
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
                key=f"away_{match['id']}",
                label_visibility="collapsed"
            )

        with col5:
            st.markdown(
                f"<div>{away_pl}</div>",
                unsafe_allow_html=True
            )

        bets[match["id"]] = {
            "home": home_goals,
            "away": away_goals
        }

        st.divider()
    
    # Zapis
    user = st.session_state["user"]

    if st.button("💾 Zapisz wszystkie typy"):
        save_user_bets(user, bets)
        st.success("Zapisano wszystkie typy!")