import streamlit as st

from app.tabs.bet_report import render_bet_report
from app.tabs.live_center import render_live_tab
from app.tabs.login import render_login
from app.tabs.submit_bets import render_submit_bets
from app.tabs.table import render_table as render_bets_table
from app.tabs.rules import render_rules


def run() -> None:
    """Render the Streamlit UI."""

    st.set_page_config(
        page_title="Zielone Zakłady 2026",
        page_icon="⚽",
        layout="centered",
    )

    if "user" not in st.session_state:
        render_login()
        st.stop()

    choice = st.sidebar.radio(
        "Menu",
        [
            "Złóż zakłady",
            "Mój raport",
            "Tabela",
            "Studio",
            "Reguły",
        ],
    )

    if choice == "Złóż zakłady":
        render_submit_bets()

    if choice == "Mój raport":
        render_bet_report()

    if choice == "Tabela":
        render_bets_table()

    if choice == "Studio":
        render_live_tab()

    if choice == "Reguły":
        render_rules()


if __name__ == "__main__":
    run()
