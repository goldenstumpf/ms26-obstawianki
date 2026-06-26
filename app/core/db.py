import os

from supabase import create_client

# load .env only for local / CLI
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


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

def get_supabase():
    url = get_secret("SUPABASE_URL")
    key = get_secret("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY")

    return create_client(url, key)

