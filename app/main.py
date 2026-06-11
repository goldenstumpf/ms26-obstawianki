import json
from datetime import datetime
import pl

import streamlit as st

st.set_page_config(
    page_title="MŚ 2026 - Typowanie",
    layout="centered"
)

st.title("⚽ MŚ 2026")

with open("app/data/matches.json", encoding="utf-8") as f:
    matches = json.load(f)

matches = [m for m in matches if m.get("matchday") == 2]

predictions = {}

for match in matches:

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
            "Gole gospodarzy",
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
            "Gole gości",
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

    predictions[match["id"]] = {
        "home": home_goals,
        "away": away_goals
    }

    st.divider()