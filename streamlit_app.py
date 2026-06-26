"""Streamlit Cloud entrypoint.

This file exists to make the project runnable from the repository root in a
package-safe way (imports via `app.*`).

Run locally:
  streamlit run streamlit_app.py

Streamlit Cloud:
  set Main file path to: streamlit_app.py
"""

from app.main import run

if __name__ == "__main__":
    run()
