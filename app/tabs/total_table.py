import streamlit as st

from core.bets import get_total_table
from utils.formatters import display_username


def render_total_table():

    st.title("Tabela Generalna")

    table = get_total_table()

    rows = []

    for i, user in enumerate(table, start=1):
        rows.append({
            "#": i,
            "Gracz": display_username(user["username"]),
            "Bety": user["bets"],
            "Punkty": user["points"],
            "Pkt / Bet": user["avg"]
        })

    st.dataframe(
        rows,
        hide_index=True,
        width="stretch"
    )