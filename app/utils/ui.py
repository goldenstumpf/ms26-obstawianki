import streamlit as st

def render_bet_native(bet, pl):
    c1, c2, c3, c4 = st.columns([2, 2, 2, 1.5])

    with c1:

        st.markdown(f"<div style='text-align:left'><img src='{bet['home_crest']}' width='18'> <small>{bet['home_code']}</small></div>", unsafe_allow_html=True)


    with c2:
        st.markdown(
            f"<div style='text-align:center; font-weight:600;'>"
            f"{bet['home']} : {bet['away']}"
            f"</div>",
            unsafe_allow_html=True
        )

        flt_home = bet.get("flt_home")
        flt_away = bet.get("flt_away")



        if flt_home is not None and flt_away is not None:
            st.markdown(
                f"""
                <div style='text-align:center; font-size:11px; color:gray; margin-top:-4px;'>
                    ({flt_home}:{flt_away})
                </div>
                """,
                unsafe_allow_html=True
            )
        
        else:
            st.markdown(
                f"""
                <div style='text-align:center; font-size:11px; color:gray; margin-top:-4px;'>
                    ({pl.format_kickoff(bet["utc_date"])})
                </div>
                """,
                unsafe_allow_html=True
            )


    with c3:
        st.markdown(f"<div style='text-align:right'><small>{bet['away_code']}</small> <img src='{bet['away_crest']}' width='18'></div>", unsafe_allow_html=True)

    with c4:
        points = bet.get("points")
        if points is not None:

            color = "chartreuse" if points > 0 else "green"
            st.markdown(
                f"<div style='text-align:center; color:{color}; font-weight:600;'>"
                f"{points}"
                f"</div>",
                unsafe_allow_html=True
            )