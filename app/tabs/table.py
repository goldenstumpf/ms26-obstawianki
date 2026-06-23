import streamlit as st
from core.bets import get_full_bets_info
from utils.formatters import format_username
from collections import defaultdict




def build_table(records: list[dict]) -> dict:
    table = defaultdict(lambda: {"matches": 0, "points": 0.0})

    for r in records:
        if not r.get("status") == "closed":
            continue

        user = r["username"]
        table[user]["matches"] += 1
        table[user]["points"] += float(r.get("points"))

    return dict(table)

def render_table():
    st.title("📋 Tabela")

    records = get_full_bets_info()
    table = build_table(records)

    if not table:
        st.info("Brak danych")
        return

    sorted_users = sorted(
        table.items(),
        key=lambda x: float(x[1].get("points") or 0),
        reverse=True
    )

    # HEADER (kompaktowy)
    st.markdown(
        """
        <div style="
            display:flex;
            font-weight:600;
            font-size:13px;
            opacity:0.7;
            margin-bottom:6px;
        ">
            <div style="width:40px">#</div>
            <div style="flex:2">Gracz</div>
            <div style="flex:1;text-align:center;">Zakłady</div>
            <div style="flex:1;text-align:center;">Pkt</div>
            <div style="flex:1;text-align:center;">Pkt/Z</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ROWS (ULTRA COMPACT)
    for i, (user, s) in enumerate(sorted_users, start=1):

        matches = s["matches"]
        points = s["points"]
        avg = points / matches if matches else 0

        st.markdown(
            f"""
            <div style="
                display:flex;
                font-size:14px;
                padding:2px 0;
                align-items:center;
            ">
                <div style="width:40px">{i}</div>
                <div style="flex:2;font-weight:500">{format_username(user)}</div>
                <div style="flex:1;text-align:center;">{matches}</div>
                <div style="flex:1;text-align:center;font-weight:600">{round(points,2)}</div>
                <div style="flex:1;text-align:center;">{round(avg,4):.4f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )