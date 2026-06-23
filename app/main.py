import streamlit as st

from tabs.login import render_login
from tabs.submit_bets import render_submit_bets
from tabs.bet_report import render_bet_report
from tabs.table import render_table as render_bets_table
from tabs.live_center import render_live_tab

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
    ["Złóż zakłady", "Mój raport", "Tabela", "Centrum - Na żywo"]
)

if choice == "Złóż zakłady":
    render_submit_bets()

if choice == "Mój raport":
    render_bet_report()

if choice == "Tabela":
    render_bets_table()

if choice == "Centrum - Na żywo":
    render_live_tab()