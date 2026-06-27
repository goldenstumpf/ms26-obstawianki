from __future__ import annotations

import streamlit as st

from app.data.full_bets_info import get_full_bets_info
from app.utils.components import KNOCKOUT_STAGES, get_points_style, render_match_row, _crest_html
from app.utils.formatters import format_username
from app.utils.match_state import classify_match_state
from app.services.score_bets import calculate_points


# =========================================================
# HELPERS
# =========================================================

def _record_map(records: list[dict]) -> dict[tuple[str, str], dict]:
    """Map (username, match_id) -> merged record."""

    out: dict[tuple[str, str], dict] = {}
    for r in records:
        u = r.get("username")
        mid = r.get("match_id")
        if not u or not mid:
            continue
        out[(str(u), str(mid))] = r
    return out


def _match_number(r: dict) -> int:
    try:
        return int(r.get("match_number") or 0)
    except Exception:
        return 0


def _is_knockout_stage(r: dict) -> bool:
    return str(r.get("stage") or "").upper() in KNOCKOUT_STAGES


def _format_knockout_suffix(dip: str | None, r: dict) -> str:
    """Compact bracket suffix: (90)/(120)/(k:{crest-or-code})."""
    if not dip:
        return ""

    d = str(dip).strip()
    if d == "90":
        return " (90)"
    if d == "120":
        return " (120)"

    dl = d.lower()
    if dl.startswith("karne"):
        rest = d[len("karne"):].strip()
        if rest.startswith(":"):
            rest = rest[1:].strip()
        code_u = (rest or "").upper()

        # In this table we keep it text-compact; crest rendering in cells is brittle in DEMO.
        return f" (k:{code_u or '?'})"

    return f" ({d})"


def _bet_text(r: dict) -> str:
    hb = r.get("home_bet")
    ab = r.get("away_bet")
    if hb is None or ab is None:
        base = "-"
    else:
        base = f"{hb}:{ab}"

    if _is_knockout_stage(r):
        base += _format_knockout_suffix(r.get("dip"), r)
    return base


def _bet_score_parts(r: dict) -> tuple[str, str | None]:
    """Return (score_text, dip_text_or_None)."""
    hb = r.get("home_bet")
    ab = r.get("away_bet")
    score = "-" if hb is None or ab is None else f"{hb}:{ab}"

    if not _is_knockout_stage(r):
        return score, None

    dip = r.get("dip")
    if not dip:
        return score, None

    d = str(dip).strip()
    if d == "90":
        return score, "90"
    if d == "120":
        return score, "120"

    if d.lower().startswith("karne"):
        rest = d[len("karne"):].strip()
        if rest.startswith(":"):
            rest = rest[1:].strip()
        code_u = (rest or "").upper() or "?"
        return score, f"k:{code_u}"

    return score, d


def _is_still_possible(r: dict) -> bool:
    """Possible iff bet does not require undoing already-scored goals.

    Rule (per user confirmation): possible if home_bet >= flt_home and away_bet >= flt_away.
    If we don't have a bet or live score, treat as possible (do not dim by default).
    """

    hb = r.get("home_bet")
    ab = r.get("away_bet")
    mh = r.get("flt_home")
    ma = r.get("flt_away")

    if hb is None or ab is None:
        return True
    if mh is None or ma is None:
        return True

    try:
        return int(hb) >= int(mh) and int(ab) >= int(ma)
    except Exception:
        return True


def _match_only_fallback(match_row: dict) -> dict:
    """Create a safe record for rendering a match card without leaking other users' bets."""

    r = dict(match_row)
    # Wipe bet-specific fields so we don't accidentally show another user's bet.
    for k in ["home_bet", "away_bet", "dip", "points", "status"]:
        if k in r:
            r[k] = None
    return r


def _card_record_for_match_id(records: list[dict], rec_map: dict[tuple[str, str], dict], username: str | None, match_id: str) -> dict | None:
    """Return the record to use for a match card: user bet row if present, otherwise match-only fallback."""

    # Prefer the logged-in user's row (may be missing if user has no bet for that match).
    if username:
        r_user = rec_map.get((str(username), str(match_id)))
        if r_user:
            return r_user

    # Fallback: any representative match row, but with bet fields wiped.
    rep = next((r for r in records if str(r.get("match_id")) == str(match_id)), None)
    if not rep:
        return None
    return _match_only_fallback(rep)


def _users(records: list[dict]) -> list[str]:
    return sorted({str(r.get("username")) for r in records if r.get("username")})


def _unique_match_ids_in_order(records: list[dict], *, predicate) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for r in sorted(records, key=_match_number):
        if not predicate(r):
            continue
        mid = str(r.get("match_id"))
        if not mid or mid in seen:
            continue
        seen.add(mid)
        out.append(mid)
    return out


def _unique_matches(records: list[dict], match_ids: list[str]) -> list[dict]:
    """Return one representative row per match_id."""
    out: list[dict] = []
    for mid in match_ids:
        row = next((r for r in records if str(r.get("match_id")) == str(mid)), None)
        if row:
            out.append(row)
    return out


def _points_value(r: dict) -> float:
    """Return points for the row.

    Alignment rule:
    - LIVE and FINISHED: use stored r['points'] (pipeline-provided)
    - Otherwise (UPCOMING/unknown): 0.0

    NOTE: We deliberately do NOT compute points on-the-fly here.
    """

    try:
        state = classify_match_state(r)
        if state in {"LIVE", "FINISHED"}:
            pts_raw = r.get("points")
            return float(pts_raw) if pts_raw is not None else 0.0
        return 0.0
    except Exception:
        return 0.0


def _sum_points_for_user(
    records: list[dict],
    username: str,
    *,
    match_ids: set[str] | None = None,
    include_live: bool = True,
    include_finished: bool = True,
) -> float:
    total = 0.0
    for r in records:
        if str(r.get("username")) != str(username):
            continue

        mid = str(r.get("match_id"))
        if match_ids is not None and mid not in match_ids:
            continue

        state = classify_match_state(r)
        if state == "LIVE" and not include_live:
            continue
        if state == "FINISHED" and not include_finished:
            continue
        if state not in {"LIVE", "FINISHED"}:
            continue

        total += _points_value(r)

    return total


def _rank_map(points_by_user: dict[str, float]) -> dict[str, int]:
    ordered = sorted(points_by_user.items(), key=lambda kv: kv[1], reverse=True)
    return {u: i + 1 for i, (u, _) in enumerate(ordered)}


def _delta_badge(prev_rank: int | None, new_rank: int | None) -> str:
    if prev_rank is None:
        return "🆕"
    if not new_rank:
        return "⚪ 0"
    diff = prev_rank - new_rank
    if diff > 0:
        return f"🟢 +{diff}"
    if diff < 0:
        return f"🔴 -{abs(diff)}"
    return "⚪ 0"


def _render_table(
    *,
    title: str,
    users: list[str],
    base_points: dict[str, float],
    new_points: dict[str, float],
    match_cols: list[dict],
    records_map: dict[tuple[str, str], dict],
    base_label: str,
    new_label: str,
    show_plus_score: bool,
    dim_impossible: bool = False,
) -> None:
    st.subheader(title)

    # Prevent header wrapping (especially for labels like 'Pkt (na żywo)').
    st.markdown(
        """
        <style>
        .lc-nowrap { white-space: nowrap; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Layout widths (keep compact to avoid wrapping). Each match becomes 2 columns:
    # - bet (score + optional DIP below)
    # - bet points
    widths = [0.55, 2.2, 0.95]
    for _ in match_cols:
        widths += [1.15, 0.55]
    widths += [1.15, 1.1]

    hdr = st.columns(widths)
    with hdr[0]:
        st.markdown("<div class='lc-nowrap' style='font-weight:600;opacity:0.7;font-size:13px;'>#</div>", unsafe_allow_html=True)
    with hdr[1]:
        st.markdown("<div class='lc-nowrap' style='font-weight:600;opacity:0.7;font-size:13px;'>Gracz</div>", unsafe_allow_html=True)
    with hdr[2]:
        st.markdown(
            f"<div class='lc-nowrap' style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>{base_label}</div>",
            unsafe_allow_html=True,
        )

    # Per-match headers: bet column shows teams, points column stays blank (or '+').
    for j, m in enumerate(match_cols):
        # Default: crests only (img : img). Fallback: HOME:AWAY codes.
        home_crest = m.get("home_crest")
        away_crest = m.get("away_crest")
        if home_crest and away_crest:
            c1 = _crest_html(home_crest, alt=str(m.get("home_code") or "home"), size_px=13)
            c2 = _crest_html(away_crest, alt=str(m.get("away_code") or "away"), size_px=13)
            label_html = f"<span>{c1}</span><span style='margin:0 4px;'>:</span><span>{c2}</span>"
        else:
            label_txt = f"{m.get('home_code') or m.get('home_team') or 'H'}:{m.get('away_code') or m.get('away_team') or 'A'}"
            label_html = label_txt

        bet_idx = 3 + (2 * j)
        pts_idx = bet_idx + 1

        with hdr[bet_idx]:
            st.markdown(
                f"<div class='lc-nowrap' style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>{label_html}</div>",
                unsafe_allow_html=True,
            )
        with hdr[pts_idx]:
            st.markdown(
                "<div class='lc-nowrap' style='font-weight:600;opacity:0.35;font-size:12px;text-align:center;'>+</div>",
                unsafe_allow_html=True,
            )

    totals_idx = 3 + (2 * len(match_cols))
    delta_idx = totals_idx + 1

    with hdr[totals_idx]:
        st.markdown(
            f"<div class='lc-nowrap' style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>{new_label}</div>",
            unsafe_allow_html=True,
        )
    with hdr[delta_idx]:
        st.markdown(
            "<div class='lc-nowrap' style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>Zmiana</div>",
            unsafe_allow_html=True,
        )

    base_rank = _rank_map(base_points)
    new_rank = _rank_map(new_points)
    ordered_users = sorted(users, key=lambda u: new_points.get(u, 0.0), reverse=True)

    bold_base = (base_label == "Pkt (pre)")

    for i, u in enumerate(ordered_users, start=1):
        cols = st.columns(widths)
        with cols[0]:
            st.markdown(f"<div style='font-size:14px;'>{i}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(
                f"<div style='font-size:14px;font-weight:500'>{format_username(u)}</div>",
                unsafe_allow_html=True,
            )
        with cols[2]:
            fw = "600" if bold_base else "400"
            st.markdown(
                f"<div style='font-size:14px;text-align:center;font-weight:{fw};'>{base_points.get(u, 0.0):.1f}</div>",
                unsafe_allow_html=True,
            )

        for j, m in enumerate(match_cols):
            mid = str(m.get("match_id"))
            r = records_map.get((u, mid), {})

            score_txt, dip_txt = _bet_score_parts(r) if r else ("-", None)
            score = _points_value(r) if r else 0.0

            bet_idx = 3 + (2 * j)
            pts_idx = bet_idx + 1

            # Dimming is handled by optional style hints passed in via 'dim_impossible'.
            dim_style = ""
            if dim_impossible and r and (not _is_still_possible(r)):
                dim_style = "opacity:0.35;"

            dip_line = (
                f"<div style='font-size:11px; margin-top:-2px; text-align:center; {dim_style}'>{dip_txt}</div>" if dip_txt else ""
            )

            with cols[bet_idx]:
                st.markdown(
                    f"<div style='font-size:14px;text-align:center; line-height:1.1; {dim_style}'>{score_txt}</div>{dip_line}",
                    unsafe_allow_html=True,
                )

            with cols[pts_idx]:
                if show_plus_score:
                    style = get_points_style(score)
                    st.markdown(
                        f"<div style='font-size:14px;text-align:center; {style} {dim_style}'>{score:.1f}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    # For last-3 tab we still show per-match points for alignment, but no (+) semantics.
                    style = get_points_style(score)
                    st.markdown(
                        f"<div style='font-size:14px;text-align:center; {style}'>{score:.1f}</div>",
                        unsafe_allow_html=True,
                    )

        totals_idx = 3 + (2 * len(match_cols))
        delta_idx = totals_idx + 1

        with cols[totals_idx]:
            total_val = new_points.get(u, 0.0)
            st.markdown(
                f"<div style='font-size:14px;text-align:center;font-weight:600;'>{total_val:.1f}</div>",
                unsafe_allow_html=True,
            )

        with cols[delta_idx]:
            badge = _delta_badge(base_rank.get(u), new_rank.get(u))
            st.markdown(f"<div style='font-size:14px;text-align:center;'>{badge}</div>", unsafe_allow_html=True)


# =========================================================
# LIVE CENTER TAB
# =========================================================

def render_live_tab() -> None:
    st.title("📺 Studio")

    records = get_full_bets_info()
    rec_map = _record_map(records)

    tab_live, tab_last3 = st.tabs(["🔴 Na żywo", "⚫ Ostatnie"])

    with tab_live:
        username = st.session_state.get("user")

        # Determine live matches using the same classifier as the bet report / match cards.
        # IMPORTANT: merged records can have bet.status overwrite match.status.
        # Therefore we filter LIVE by classify_match_state() and do not use minute heuristics.
        def _is_live_match(r: dict) -> bool:
            return classify_match_state(r) == "LIVE"

        live_ids = _unique_match_ids_in_order(records, predicate=_is_live_match)
        live_matches = _unique_matches(records, live_ids)

        if live_matches:
            for m in sorted(live_matches, key=_match_number):
                mid = str(m.get("match_id"))
                r_card = _card_record_for_match_id(records, rec_map, username, mid)
                if r_card:
                    render_match_row(r_card, mode="view")
        else:
            st.info("Brak meczów na żywo")

        dim_impossible = st.toggle(
            "Podświetl aktywne",
            value=False,
            help="Gdy włączone: wyróżnia te zakłady, które wciąż mogą trafić dokładny wynik.",
        )

        users = _users(records)
        base_points = {u: _sum_points_for_user(records, u, include_live=False, include_finished=True) for u in users}
        new_points = {u: _sum_points_for_user(records, u, include_live=True, include_finished=True) for u in users}

        _render_table(
            title="Tabela (na żywo)",
            users=users,
            base_points=base_points,
            new_points=new_points,
            match_cols=live_matches[:4],
            records_map=rec_map,
            base_label="Pkt (pre)",
            new_label="Pkt (na żywo)",
            show_plus_score=True,
            dim_impossible=dim_impossible,
        )

    with tab_last3:
        finished_ids = _unique_match_ids_in_order(records, predicate=lambda r: classify_match_state(r) == "FINISHED")
        last3_ids = finished_ids[-3:]
        last3_matches = _unique_matches(records, last3_ids)

        if not last3_matches:
            st.info("Brak zakończonych meczów")
            return

        # Render the SAME matches as in the table below, sorted ascending by match_number.
        # Always render 3 cards; if the user has no bet for a match, fall back to match-only card (no bet leakage).
        username = st.session_state.get("user")
        for m in sorted(last3_matches, key=_match_number):
            mid = str(m.get("match_id"))
            r_card = _card_record_for_match_id(records, rec_map, username, mid)
            if r_card:
                render_match_row(r_card, mode="view")

        users = _users(records)
        last3_set = {str(m.get("match_id")) for m in last3_matches}

        total_finished = {u: _sum_points_for_user(records, u, include_live=False, include_finished=True) for u in users}
        pts_last3 = {
            u: _sum_points_for_user(records, u, match_ids=last3_set, include_live=False, include_finished=True) for u in users
        }

        before_points = {u: (total_finished.get(u, 0.0) - pts_last3.get(u, 0.0)) for u in users}
        after_points = total_finished

        _render_table(
            title="Tabela (ostatnie 3 mecze)",
            users=users,
            base_points=before_points,
            new_points=after_points,
            match_cols=last3_matches,
            records_map=rec_map,
            base_label="Pkt (pre)",
            new_label="Pkt (post)",
            show_plus_score=False,
        )
