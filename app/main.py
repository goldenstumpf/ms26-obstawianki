import streamlit as st

from tabs.login import render_login
from tabs.submit_bets import render_submit_bets

if "user" not in st.session_state:
    render_login()
    st.stop()

choice = st.sidebar.radio(
    "Menu",
    ["Złóż zakłady", "Moje zakłady", "Tabela"]
)

if choice == "Złóż zakłady":
    render_submit_bets()
