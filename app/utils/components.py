import streamlit as st

from pathlib import Path

from app.data.demo import demo_mode_enabled
from app.utils import i18n as pl
from app.utils.time import format_datetime, parse_kickoff

# -------------------------
# DIP / KNOCKOUT HELPERS
# -------------------------

KNOCKOUT_STAGES = {
    "FINAL",
    "THIRD_PLACE",
    "SEMI_FINALS",
    "QUARTER_FINALS",
    "LAST_16",
    "LAST_32",
    "LAST_64",
}


def _is_knockout_stage(r: dict) -> bool:
    return str(r.get("stage") or "").upper() in KNOCKOUT_STAGES


def _parse_penalty_dip(dip: str | None) -> str | None:
    """Return team code after 'karne:' if dip is penalty-type."""
    if not dip:
        return None
    d = str(dip).strip()
    if not d.lower().startswith("karne"):
        return None
    # Accept: "karne: GER" or "karne GER"
    d = d.replace("karne", "", 1).strip()
    if d.startswith(":"):
        d = d[1:].strip()
    return d or None


def _penalty_winner_code(match: dict) -> str | None:
    """Resolve winner code using penalties when available.

    Falls back to pre-penalties final score (flt) if penalty scores are missing.
    """
    ph = match.get("pens_home")
    pa = match.get("pens_away")
    if ph is not None and pa is not None:
        if ph > pa:
            return match.get("home_code")
        if pa > ph:
            return match.get("away_code")
        return None

    # fallback
    mh = match.get("flt_home")
    ma = match.get("flt_away")
    if mh is None or ma is None:
        return None
    if mh > ma:
        return match.get("home_code")
    if ma > mh:
        return match.get("away_code")
    return None


def _resolve_demo_crest_url(crest_url: str | None) -> str | None:
    """Normalize demo crest references to a browser-loadable URL.

    In DEMO_MODE we must remain network-free.

    Streamlit serves files placed under `.streamlit/static/...` at `/static/...`.
    In some deployments (reverse proxies), the app is mounted under a base path
    like `/app`, making the effective static path `/app/static/...`.

    We must not emit filesystem paths (e.g. `.streamlit/static...`) into an
    `<img src=...>` attribute. Prefer returning a base-path-safe (relative) URL
    when mapping local files.
    """
    if not crest_url:
        return None

    url = str(crest_url).strip().replace("\\", "/")

    # If the caller already provided a served URL, keep it as-is.
    if url.startswith("/static/") or url.startswith("/app/static/"):
        return url

    # If something passed a local-ish path, convert it to a served URL.
    if url.startswith(".streamlit/static/"):
        rel = url[len(".streamlit/static/") :]
        # Relative URL works under both `/static/...` and `/app/static/...` mounts.
        return f"static/{rel}"

    # If only a filename is provided, serve from the known crests dir when possible.
    if "/" not in url:
        pf = Path(".streamlit") / "static" / "crests" / url
        if pf.exists():
            return f"static/crests/{url}"

    return None

def _crest_html(crest_url: str | None, *, alt: str = "", size_px: int = 18) -> str:
    """Return a small inline crest HTML.

    Prefer <img> over inline <svg> to avoid Streamlit escaping/sanitization issues.

    NOTE: In this Streamlit setup, requests to `/static/...` may return the
    Streamlit HTML shell (200 text/html) instead of the actual file bytes.
    In DEMO_MODE we therefore embed local SVGs as data URIs.
    """
    if not crest_url:
        return ""

    url = str(crest_url).strip().replace("\\", "/")

    if demo_mode_enabled():
        import base64

        local_file: Path | None = None

        # Filename only -> `.streamlit/static/crests/{filename}`
        if "/" not in url:
            candidate = Path(".streamlit") / "static" / "crests" / url
            if candidate.exists():
                local_file = candidate

        # Served-like URL -> map back to `.streamlit/static/...`
        if local_file is None:
            if url.startswith("/static/"):
                candidate = Path(".streamlit") / "static" / url[len("/static/") :]
                if candidate.exists():
                    local_file = candidate
            elif url.startswith("/app/static/"):
                candidate = Path(".streamlit") / "static" / url[len("/app/static/") :]
                if candidate.exists():
                    local_file = candidate
            elif url.startswith("static/"):
                candidate = Path(".streamlit") / "static" / url[len("static/") :]
                if candidate.exists():
                    local_file = candidate
            elif url.startswith(".streamlit/static/"):
                candidate = Path(url)
                if candidate.exists():
                    local_file = candidate

        if local_file is not None and local_file.suffix.lower() == ".svg":
            svg_text = local_file.read_text(encoding="utf-8")
            b64 = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
            url = f"data:image/svg+xml;base64,{b64}"
        else:
            demo_url = _resolve_demo_crest_url(url)
            if demo_url:
                url = demo_url

    return (
        f"<img src=\"{url}\" alt=\"{alt}\" "
        f"style=\"height:{size_px}px;width:{size_px}px;vertical-align:middle;\" />"
    )


def _format_dip_display(dip: str | None, r: dict, *, prefer_crest: bool = True) -> str | None:
    """Format a DIP value for display (as HTML-safe string)."""
    if not dip:
        return None

    d = str(dip).strip()
    if d == "90":
        return "w 90 minut"
    if d == "120":
        return "po dogrywce"

    code = _parse_penalty_dip(d)
    if code:
        code_u = code.upper()
        home_code = str(r.get("home_code") or "").upper()
        away_code = str(r.get("away_code") or "").upper()

        crest = ""
        if prefer_crest:
            if code_u and code_u == home_code:
                crest = _crest_html(r.get("home_crest"), alt=home_code)
            elif code_u and code_u == away_code:
                crest = _crest_html(r.get("away_crest"), alt=away_code)

        if crest:
            return f"karne: {crest}"
        return f"karne: {code_u}"

    return d


def _actual_dip_display(r: dict) -> str | None:
    """Return display DIP for the actual match outcome (knockout only)."""
    if not _is_knockout_stage(r):
        return None

    duration = r.get("duration")
    if duration == "EXTRA_TIME":
        return "po dogrywce"
    if duration == "PENALTY_SHOOTOUT":
        winner = _penalty_winner_code(r)
        if not winner:
            return "karne"
        winner_u = str(winner).upper()
        if winner_u == str(r.get("home_code") or "").upper():
            crest = _crest_html(r.get("home_crest"), alt=winner_u)
            return f"karne: {crest}" if crest else f"karne: {winner_u}"
        if winner_u == str(r.get("away_code") or "").upper():
            crest = _crest_html(r.get("away_crest"), alt=winner_u)
            return f"karne: {crest}" if crest else f"karne: {winner_u}"
        return f"karne: {winner_u}"

    return "w 90 minut"


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
        elif r.get("status") in ["closed", "FINISHED"]:
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
        crest_left = r.get("home_crest")
        if demo_mode_enabled():
            crest_left = _resolve_demo_crest_url(crest_left) or crest_left

        # Single HTML row to avoid nested columns (which caused stray '0' artifacts)
        crest_html = _crest_html(crest_left, alt=str(r.get("home_code") or "home"), size_px=18) if crest_left else ""
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:6px; justify-content:flex-start;'>"
            f"{crest_html}<span>{home_pl}</span>"
            f"</div>",
            unsafe_allow_html=True,
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
        # DIP (knockout only)
        # -------------------------
        # -------------------------
        # DIP (knockout only)
        # -------------------------
        if _is_knockout_stage(r):
            dip_key = f"dip_{match_id}"
            if dip_key not in st.session_state:
                st.session_state[dip_key] = r.get("dip")

            bh = st.session_state.get(home_key)
            ba = st.session_state.get(away_key)

            # Only show DIP when both bets are set (then DIP is required)
            if bh is not None and ba is not None:
                dip_options: list[str]
                dip_labels: dict[str, str]

                if int(bh) == int(ba):
                    hc = str(r.get("home_code") or "HOME")
                    ac = str(r.get("away_code") or "AWAY")
                    o1 = f"karne: {hc}"
                    o2 = f"karne: {ac}"
                    dip_options = [o1, o2]
                    dip_labels = {o1: o1, o2: o2}
                    default = o1
                else:
                    dip_options = ["90", "120"]
                    dip_labels = {"90": "w 90 minut", "120": "po dogrywce"}
                    default = "90"

                current = st.session_state.get(dip_key)
                if current is None or str(current) not in dip_options:
                    current = default
                    st.session_state[dip_key] = default

                st.selectbox(
                    "DIP",
                    options=dip_options,
                    index=dip_options.index(str(current)),
                    key=f"_ui_{dip_key}",
                    help=(
                        "Dodatkowa Informacja Pucharowa (DIP) jest wymagana dla meczów pucharowych. "
                        "Jeśli typujesz zwycięstwo (win/lose), wybierz czy rozstrzygnięcie nastąpi w 90 czy w 120 minut. "
                        "Jeśli typujesz remis, wybierz kto wygra w karnych."
                    ),
                    format_func=lambda x: dip_labels.get(x, str(x)),
                )

                sel = st.session_state.get(f"_ui_{dip_key}")
                st.session_state[dip_key] = sel

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

            bet_html = f"<div style='text-align:center'>{home_text} : {away_text}</div>"
            st.markdown(bet_html, unsafe_allow_html=True)

            # DIP UNDER BET (knockout only, if exists)
            dip_txt = _format_dip_display(r.get("dip"), r)
            if dip_txt and _is_knockout_stage(r):
                st.markdown(
                    f"<div style='text-align:center; font-size:12px; margin-top:-2px;'>{dip_txt}</div>",
                    unsafe_allow_html=True,
                )



        # FINAL SCORE UNDER ENTIRE ROW
        if has_result:
            actual_dip = _actual_dip_display(r)
            suffix = f" | {actual_dip}" if actual_dip else ""
            st.markdown(
                f"<div style='text-align:center; font-size:12px; color:gray; margin-top:-8px;'>({r.get('flt_home')} : {r.get('flt_away')}{suffix})</div>",
                unsafe_allow_html=True,
            )

    with col5:
        crest_right = r.get("away_crest")
        if demo_mode_enabled():
            crest_right = _resolve_demo_crest_url(crest_right) or crest_right

        crest_html = _crest_html(crest_right, alt=str(r.get("away_code") or "away"), size_px=18) if crest_right else ""
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:6px; justify-content:flex-end;'>"
            f"<span>{away_pl}</span>{crest_html}"
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