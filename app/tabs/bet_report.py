import streamlit as st

from app.data.full_bets_info import get_full_bets_info
from app.utils.components import render_match_row

# -----------------------------
# FILTER LOGIC
# -----------------------------

LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT",
}


def is_relevant_match(r: dict, include_upcoming: bool) -> bool:
    is_bet = (
        r.get("home_bet") is not None
        and r.get("away_bet") is not None
    )

    has_result = (
        r.get("flt_home") is not None
        and r.get("flt_away") is not None
    )

    if include_upcoming:
        return is_bet or has_result

    return has_result


# -----------------------------
# SORTING
# -----------------------------

def sort_matches(records: list[dict], mode: str) -> list[dict]:
    """
    Stabilne sortowanie raportu betów.

    Tryb "Od najbliższych" sortuje kategoriami:
    1) nadchodzące (od najbliższego terminu),
    2) na żywo,
    3) zakończone (od najnowszego).
    """

    def safe_points(r):
        return r.get("points") if r.get("points") is not None else -1

    def safe_date(r):
        # fallback żeby None nie rozwalało sortowania
        return r.get("utc_date") or ""

    def has_result(r: dict) -> bool:
        return r.get("flt_home") is not None and r.get("flt_away") is not None

    def is_live(r: dict) -> bool:
        return r.get("status") in LIVE_STATUSES

    if mode == "Od najbliższych 🕒":
        upcoming = [r for r in records if (not has_result(r)) and (not is_live(r))]
        live = [r for r in records if (not has_result(r)) and is_live(r)]
        finished = [r for r in records if has_result(r)]

        # upcoming: closest kickoff first (ascending)
        upcoming = sorted(upcoming, key=safe_date)
        # live: keep consistent ordering
        live = sorted(live, key=safe_date)
        # finished: same as "Od najnowszych" (descending)
        finished = sorted(finished, key=safe_date, reverse=True)

        return upcoming + live + finished

    if mode == "Od najnowszych ⏳":
        return sorted(records, key=safe_date, reverse=True)

    if mode == "Od najstarszych ⌛":
        return sorted(records, key=safe_date)

    if mode == "Od najlepszych 📈":
        return sorted(records, key=safe_points, reverse=True)

    if mode == "Od najsłabszych 📉":
        return sorted(records, key=safe_points)

    return records


# -----------------------------
# MAIN VIEW
# -----------------------------

def render_bet_report():
    st.title("📊 Mój raport")
    st.caption("Historia Twoich zakładów")

    username = st.session_state.get("user")

    if not username:
        st.warning("Brak użytkownika w sesji")
        return

    # -------------------------
    # DATA
    # -------------------------
    records = [
        r for r in get_full_bets_info()
        if r.get("username") == username
    ]

    # -------------------------
    # UI CONTROLS
    # -------------------------
    sort_mode = st.selectbox(
        "Sortowanie",
        [
            "Od najbliższych 🕒",
            "Od najnowszych ⏳",
            "Od najstarszych ⌛",
            "Od najlepszych 📈",
            "Od najsłabszych 📉",
        ],
        index=0,
    )

    show_upcoming = st.toggle(
        "📅 Pokazuj nadchodzące mecze",
        value=False
    )

    # -------------------------
    # FILTER LOGIC
    # -------------------------
    records = [
        r for r in records
        if is_relevant_match(r, show_upcoming)
    ]

    # -------------------------
    # SORTING
    # -------------------------
    records = sort_matches(records, sort_mode)

    st.divider()

     # -------------------------
    # EMPTY STATE
    # -------------------------
    if not records:
        st.info("Brak danych do wyświetlenia.")
        return

    # -------------------------
    # RENDER
    # -------------------------
    for r in records:
        render_match_row(r, mode="view")
