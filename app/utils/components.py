import streamlit as st

import core.i18n as pl
from utils.time import format_datetime, parse_kickoff

def _has_final_score(r: dict) -> bool:
    return r.get("flt_home") is not None and r.get("flt_away") is not None

def get_points_style(points):
    if points is None:
        return ""

    if points >= 4:
        return "color:#00c853;font-weight:600;"  # jasna zieleń
    if points > 0:
        return "color:#D4AF37;font-weight:500;"  # ciemna zieleń 

    return "color:#808080;"


def render_match_row(r: dict, mode: str = "edit"):
    """
    mode:
    - "edit" → number inputs (betting)
    - "view" → read-only (report)
    """

    minute = r["minute"]

    match_id = str(r["match_id"])

    home_pl = pl.country(r["home_team"])
    away_pl = pl.country(r["away_team"])

    stage_pl = pl.stage(r.get("stage", ""))
    group_pl = pl.group(r.get("group_name", ""))

    date_pl = format_datetime(parse_kickoff(r["utc_date"]))

    is_bet = r.get("home_bet") is not None and r.get("away_bet") is not None

    # -------------------------
    # HEADER STATUS
    # -------------------------
    if mode == "edit":
        if is_bet:
            st.success("✔ Obstawione")
        else:
            st.info("✏️ Do obstawienia")

    else:
        if r.get("status") == "live":
            st.markdown("")
            if minute:
                st.markdown(
                    f"""
                    <div>
                        🔴 Na żywo
                        <span style="color:red; font-weight:600; text-align:center; margin-left:24px;">
                            {minute}'
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
               st.markdown("🔴 Na żywo") 
        elif r.get("status") == "closed":
            st.markdown("⚫ Zakończony")
        else:
            st.markdown("🟡 Nadchodzący")

    # -------------------------
    # META
    # -------------------------
    st.caption(
        f"MECZ #{r['match_number']} | "
        f"{group_pl or stage_pl} | "
        f"{date_pl}"
    )

    # -------------------------
    # ROW LAYOUT
    # -------------------------
    if mode == "edit":
        col1, col2, col3, col4, col5 = st.columns([5, 1.2, 0.5, 1.2, 5])
    else:
        col1, col3, col5 = st.columns([5, 2, 5])

    with col1:
        st.markdown(
            f"<div style='text-align:left'>"
            f"<img src='{r['home_crest']}' width='20'> {home_pl}"
            f"</div>", unsafe_allow_html=True,
            )

    # -------------------------
    # EDIT MODE
    # -------------------------
    if mode == "edit":

        home_key = f"home_{match_id}"
        away_key = f"away_{match_id}"

        if home_key not in st.session_state:
            st.session_state[home_key] = r.get("home_bet")

        if away_key not in st.session_state:
            st.session_state[away_key] = r.get("away_bet")

        with col2:
            st.number_input(
                "home_goals",
                min_value=0,
                step=1,
                key=home_key,
                label_visibility="collapsed",
            )

        with col3:
            st.markdown(
                f"<div style='text-align:center'>"
                f":"
                f"</div>",
            unsafe_allow_html=True,
        )

        with col4:
            st.number_input(
                "away_goals",
                min_value=0,
                step=1,
                key=away_key,
                label_visibility="collapsed",
            )

    # -------------------------
    # VIEW MODE
    # -------------------------
    else:

        has_result = r.get("flt_home") is not None and r.get("flt_away") is not None

        home_bet = r.get("home_bet")
        away_bet = r.get("away_bet")


        # MIDDLE
        with col3:
            if home_bet is None:
                home_text = "-"
            else:
                home_text = str(home_bet)
            if away_bet is None:
                away_text = "-"
            else:
                away_text = str(away_bet)

            st.markdown(
                f"<div style='text-align:center'>{home_text} : {away_text}</div>",
                unsafe_allow_html=True,
            )



        # FINAL SCORE UNDER ENTIRE ROW
        if has_result:
            st.markdown(
                f"""
                <div style="text-align:center; font-size:12px; color:gray; margin-top:-8px;">
                    ({r.get('flt_home')} : {r.get('flt_away')})
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col5:
        st.markdown(
            f"<div style='text-align:right'>"
            f"{away_pl} <img src='{r['away_crest']}' width='20'>"
            f"</div>",  
            unsafe_allow_html=True,
        )

    # -------------------------
    # FOOTER (only report mode)
    # -------------------------
    if mode == "view" and r.get("points") is not None:
        style = get_points_style(r["points"])

        st.markdown(
            f"""
            <div style="text-align:left; margin-top:6px; {style}">
                🏆 {r['points']} pkt
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()