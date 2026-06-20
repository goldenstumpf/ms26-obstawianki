import os
from dotenv import load_dotenv

# load .env only for local / CLI
load_dotenv()


def get_secret(key: str):
    """
    Priority:
    1. Streamlit Cloud / runtime secrets
    2. Local .env / environment variables
    """

    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.getenv(key)