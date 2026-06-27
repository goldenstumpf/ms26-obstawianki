import streamlit as st

from app.data.users import authenticate_user


def render_login() -> None:

    st.title("Login")

    nick = st.text_input("Nick")
    pin = st.text_input("PIN", type="password")

    if st.button("Zaloguj"):
        if authenticate_user(nick, pin):
            st.session_state["user"] = nick
            st.success("OK")
            st.rerun()
        else:
            st.error("Błędny login")
