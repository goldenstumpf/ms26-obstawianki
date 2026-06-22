import streamlit as st

from tabs.login import render_login
from tabs.submit_bets import render_submit_bets
from tabs.bet_report import render_bet_report
#from tabs.total_table import render_bets_table
from tabs.table import render_table as render_bets_table


st.set_page_config(
    page_title="Zielone Zakłady 2026",
    page_icon="⚽",
    layout="centered"
)

if "user" not in st.session_state:
    render_login()
    st.stop()

choice = st.sidebar.radio(
    "Menu",
    ["Złóż zakłady", "Mój raport", "Tabela"]
)

if choice == "Złóż zakłady":
    render_submit_bets()

if choice == "Mój raport":
    #render_bet_report()
    render_bet_report()


if choice == "Tabela":
    render_bets_table()