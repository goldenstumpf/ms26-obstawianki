import os

def get_secret(key: str):
    """
    1. Streamlit cloud/local -> st.secrets
    2. GitHub Actions / local scripts -> os.getenv
    """

    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv(key)