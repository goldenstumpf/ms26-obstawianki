from __future__ import annotations

import streamlit as st

from app.data.bets import list_bets_map_for_user, upsert_bets_for_user
from app.data.matches import list_bettable_matches
from app.utils.components import render_match_row


def render_submit_bets() -> None:

    st.title("⚽ Złóż zakłady")
    st.caption("Typuj wyniki meczów z nadchodzących 72 godzin.")
    st.divider()

    username = st.session_state["user"]

    # -------------------------
    # DATA (targeted)
    # -------------------------
    matches = list_bettable_matches(hours=72)
    bets_map = list_bets_map_for_user(username)

    # merge match + bet (for this user only)
    records: list[dict] = []
    for m in matches:
        mid = str(m["match_id"])
        record = {**m, **bets_map.get(mid, {}), "username": username}
        records.append(record)

    records.sort(key=lambda r: int(r.get("match_number") or 0))

    # -------------------------
    # SPLIT
    # -------------------------
    unbet_records = [r for r in records if r.get("home_bet") is None]
    bet_records = [r for r in records if r.get("home_bet") is not None]

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

    st.info("Możesz aktualizować zakłady do rozpoczęcia meczu.")

    st.subheader("✅ Już obstawione")

    for r in bet_records:
        render_match_row(r, mode="edit")

    # -------------------------
    # SAVE PAYLOAD
    # -------------------------
    bets_payload: dict[str, dict[str, int | None | str]] = {}

    for r in records:
        match_id = str(r["match_id"])
        bets_payload[match_id] = {
            "home_bet": st.session_state.get(f"home_{match_id}"),
            "away_bet": st.session_state.get(f"away_{match_id}"),
            "dip": st.session_state.get(f"dip_{match_id}"),
        }

    # -------------------------
    # SAVE BUTTON
    # -------------------------
    st.info("Zapis zmienia tylko nowe lub zmodyfikowane zakłady.")

    if st.button("💾 Zapisz wszystkie zakłady", use_container_width=True):
        result = upsert_bets_for_user(username=username, bets=bets_payload)

        st.success(f"✔ Zapisano zmian: {result['changed']}")

        if result.get("skipped", 0) > 0:
            st.warning(f"Pominięto: {result['skipped']}")
