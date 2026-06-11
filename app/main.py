import streamlit as st
from core.bets import init_db

from tabs.login import render_login
from tabs.submit_bets import render_submit_bets

init_db()

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
    ["Złóż zakłady", "Moje zakłady", "Tabela"]
)

if choice == "Złóż zakłady":
    render_submit_bets()
