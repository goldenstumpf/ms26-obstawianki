from core.bets import get_full_bets_info, save_bets
from core.matches import get_bettable_matches
from utils.components import render_match_row
import streamlit as st


def render_submit_bets():

    st.title("⚽ Złóż zakłady")
    st.caption("Typuj wyniki meczów z nadchodzących 72 godzin.")
    st.divider()

    username = st.session_state["user"]

    # -------------------------
    # DATA
    # -------------------------
    records = [
        r for r in get_full_bets_info()
        if r["username"] == username
    ]

    records = get_bettable_matches(records)

    # -------------------------
    # SPLIT
    # -------------------------
    unbet_records = [
        r for r in records
        if r.get("home_bet") is None
    ]

    bet_records = [
        r for r in records
        if r.get("home_bet") is not None
    ]

    # -------------------------
    # SECTION 1
    # -------------------------
    st.subheader("📝 Do obstawienia")

    for r in unbet_records:
        render_match_row(r, mode="edit")

    # -------------------------
    # SECTION 2
    # -------------------------
    if unbet_records and bet_records:
        st.divider()

    st.info(
        "Możesz aktualizować zakłady do rozpoczęcia meczu."
    )

    st.subheader("✅ Już obstawione")

    for r in bet_records:
        render_match_row(r, mode="edit")

    # -------------------------
    # SAVE PAYLOAD
    # -------------------------
    bets = {}

    for r in records:
        match_id = str(r["match_id"])

        bets[match_id] = {
            "home_bet": st.session_state.get(f"home_{match_id}"),
            "away_bet": st.session_state.get(f"away_{match_id}"),
        }

    # -------------------------
    # SAVE BUTTON
    # -------------------------
    st.info("Zapis zmienia tylko nowe lub zmodyfikowane zakłady.")

    if st.button("💾 Zapisz wszystkie zakłady", use_container_width=True):

        result = save_bets(
            username=username,
            bets=bets,
        )

        st.success(f"✔ Zapisano zmian: {result['changed']}")

        if result["skipped"] > 0:
            st.warning(f"Pominięto: {result['skipped']}")