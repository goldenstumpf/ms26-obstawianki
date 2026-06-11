import streamlit as st
from core.users import authenticate

def render_login():

    st.title("Login")

    nick = st.text_input("Nick")
    pin = st.text_input("PIN", type="password")

    if st.button("Zaloguj"):
        if authenticate(nick, pin):
            st.session_state["user"] = nick
            st.success("OK")
            st.rerun()
        else:
            st.error("Błędny login")