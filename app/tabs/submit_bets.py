import streamlit as st
from core.matches import get_matches, get_bettable_matches
from core.bets import get_bets, save_bets
from utils import pl_translations as pl


def render_submit_bets():

    st.title("Złóż zakłady")
    st.caption("Typuj wyniki meczów z nadchodzących 72 godzin.")
    st.divider()

    matches = get_matches()

    # Filtrowanie meczów
    matches_to_bet = get_bettable_matches(matches)

    username = st.session_state["user"]
    user_bets = get_bets(username)    
    user_bets_dict = {b["match_id"]: b for b in user_bets}

    bets = {}

    for match in matches_to_bet:

        match_id = match["match_id"]

        # Sprawdzenie, czy już obstawione
        existing = user_bets_dict.get(str(match_id), {})
        is_bet = str(match_id) in user_bets_dict

        home_key = f"home_{match_id}"
        away_key = f"away_{match_id}"

        if home_key not in st.session_state:
            st.session_state[home_key] = existing.get("home", None)

        if away_key not in st.session_state:
            st.session_state[away_key] = existing.get("away", None)

        home_pl = pl.country(match["home_team"])
        away_pl = pl.country(match["away_team"])

        home_img = match['home_crest']
        away_img = match['away_crest']
        
        stage_pl = pl.stage(match.get("stage", ""))
        group_pl = pl.group(match.get("group_name", ""))

        date_pl = pl.format_kickoff(match["utc_date"])

        if is_bet:
            st.success("✔ Obstawione")
        else:
            st.info("✏️ Do obstawienia")

        st.caption(
            f"MECZ #{match['match_number']} | {group_pl or stage_pl} | {date_pl}"
        )

        col1, col2, col3, col4, col5 = st.columns(
            [5, 1.2, 0.5, 1.2, 5]
        )

        with col1:
            st.markdown(
                f"<div style='text-align:right'>{home_pl} <img src='{home_img}' width='20'></div>",
                #f"<div style='text-align:right'>{home_pl}</div>", Prostsza wersja
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
                f"<div style='text-align:left'><img src='{away_img}' width='20'> {away_pl}</div>",
                unsafe_allow_html=True
            )

        bets[str(match_id)] = {
            "home": home_goals,
            "away": away_goals
        }

        st.divider()

    attempted = len(bets)
    
    # Zapis

    if st.button("💾 Zapisz wszystkie typy"):

        result = save_bets(
            username,
            bets,
            matches_to_bet
        )


        st.success(f"✔ Zapisano zmian: {result['changed']}")

        if result["skipped"] > 0:
            st.warning(f"Pominięto: {result['skipped']} (brak danych / nieprawidłowe)")

        # Nie przygotowano funkcjonalności informacji nt. pominięcia rozpoczętych meczów przy zapisie.
        #if result["skipped"] > 0:
        #    st.warning(f"✔ Zapisano tylko: {saved} typów ({skipped} z meczów już rozpoczęto).")