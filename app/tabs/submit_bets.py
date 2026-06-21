import streamlit as st

from core.bets import get_full_bets_info, save_bets
from core.matches import get_bettable_matches
import core.i18n as pl
from utils.time import format_datetime, parse_kickoff


def _render_matches_section(
    title: str,
    records: list[dict],
) -> None:
    if not records:
        return

    st.subheader(title)

    for r in records:
        match_id = str(r["match_id"])

        home_key = f"home_{match_id}"
        away_key = f"away_{match_id}"

        # Initialize state once
        if home_key not in st.session_state:
            st.session_state[home_key] = r.get("home_bet")

        if away_key not in st.session_state:
            st.session_state[away_key] = r.get("away_bet")

        is_bet = (
            r.get("home_bet") is not None
            and r.get("away_bet") is not None
        )

        home_pl = pl.country(r["home_team"])
        away_pl = pl.country(r["away_team"])

        stage_pl = pl.stage(r.get("stage", ""))
        group_pl = pl.group(r.get("group_name", ""))

        date_pl = format_datetime(
            parse_kickoff(r["utc_date"])
        )

        if is_bet:
            st.success("✔ Obstawione")
        else:
            st.info("✏️ Do obstawienia")

        st.caption(
            f"MECZ #{r['match_number']} | "
            f"{group_pl or stage_pl} | "
            f"{date_pl}"
        )

        col1, col2, col3, col4, col5 = st.columns(
            [5, 1.2, 0.5, 1.2, 5]
        )

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
            st.number_input(
                "Gole gospodarzy",
                min_value=0,
                step=1,
                key=home_key,
                label_visibility="collapsed",
            )

        with col3:
            st.markdown(
                "<div style='text-align:center;padding-top:8px'>:</div>",
                unsafe_allow_html=True,
            )

        with col4:
            st.number_input(
                "Gole gości",
                min_value=0,
                step=1,
                key=away_key,
                label_visibility="collapsed",
            )

        with col5:
            st.markdown(
                (
                    f"<div style='text-align:left'>"
                    f"<img src='{r['away_crest']}' width='20'> "
                    f"{away_pl}"
                    f"</div>"
                ),
                unsafe_allow_html=True,
            )

        st.divider()


def render_submit_bets():
    st.title("⚽ Złóż zakłady")
    st.caption("Typuj wyniki meczów z nadchodzących 72 godzin.")
    st.divider()

    username = st.session_state["user"]

    # Full view
    records = [
        r
        for r in get_full_bets_info()
        if r["username"] == username
    ]

    # Only matches available for betting
    records = get_bettable_matches(records)

    # Keep existing ordering
    unbet_records = [
        r
        for r in records
        if (
            r.get("home_bet") is None
            and r.get("away_bet") is None
        )
    ]

    bet_records = [
        r
        for r in records
        if (
            r.get("home_bet") is not None
            and r.get("away_bet") is not None
        )
    ]

    _render_matches_section(
        "📝 Do obstawienia",
        unbet_records,
    )

    if unbet_records and bet_records:
        st.divider()

    st.info(
        "Poniższe mecze zostały już obstawione, ale zakłady mogą zostać zaktualizowane do godziny rozpoczęcia meczu."
        )

    _render_matches_section(
        "✅ Już obstawione",
        bet_records,
    )
    
    # Build payload directly from current UI state
    bets = {}

    for r in records:
        match_id = str(r["match_id"])

        bets[match_id] = {
            "home_bet": st.session_state.get(
                f"home_{match_id}"
            ),
            "away_bet": st.session_state.get(
                f"away_{match_id}"
            ),
        }

    st.info(
        "Zapisane zostaną wszystkie nowe i zaktualizowane zakłady widoczne na tej stronie. "
        "Niezmienione i nieobstawione mecze zostaną pominięte."
    )

    if st.button(
        "💾 Zapisz wszystkie typy",
        use_container_width=True,
    ):
        result = save_bets(
            username=username,
            bets=bets,
        )

        st.success(
            f"✔ Zapisano zmian: {result['changed']}"
        )

        if result["skipped"] > 0:
            st.warning(
                f"Pominięto: {result['skipped']} "
                "(brak kompletnego zakładu)"
            )