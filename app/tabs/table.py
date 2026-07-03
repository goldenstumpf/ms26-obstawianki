from collections import defaultdict

import streamlit as st

from app.data.full_bets_info import get_full_bets_info
from app.utils.formatters import format_username
from app.utils.match_state import classify_match_state
from app.utils.components import KNOCKOUT_STAGES, get_points_style


BUCKET_INT_VALUES: list[int] = [5, 4, 3, 2, 1]
BUCKET_HALF_KEY: str = "+0.5"
def _ensure_sort_state() -> None:
    if "table_sort_key" not in st.session_state:
        st.session_state["table_sort_key"] = "points"  # default
    if "table_sort_dir" not in st.session_state:
        st.session_state["table_sort_dir"] = "desc"  # 'asc' | 'desc'


def _set_sort(key: str, direction: str) -> None:
    st.session_state["table_sort_key"] = key
    st.session_state["table_sort_dir"] = direction



def _toggle_sort(key: str) -> None:
    current_key = st.session_state.get("table_sort_key")
    current_dir = st.session_state.get("table_sort_dir", "desc")

    if current_key == key:
        # toggle direction
        st.session_state["table_sort_dir"] = ("asc" if current_dir == "desc" else "desc")
        return

    # switch column; keep current dir if present, otherwise default to desc
    st.session_state["table_sort_key"] = key
    st.session_state["table_sort_dir"] = current_dir or "desc"


def _sort_toggle_button(key: str) -> None:
    """Single toggle sort button used in the buttons row.

    - Click toggles sort direction for the active key.
    - Clicking a different key switches sort column (keeps current direction).
    """

    _ensure_sort_state()

    current_key = st.session_state.get("table_sort_key")
    current_dir = st.session_state.get("table_sort_dir", "desc")

    # Arrow-only labels to avoid wrapping and keep the row compact.
    # Active column shows its direction; inactive shows both arrows.
    if current_key == key:
        label = "▲" if current_dir == "asc" else "▼"
    else:
        label = "▲/▼"

    if st.button(label, key=f"table_sort_toggle_{key}"):
        _toggle_sort(key)
        # Force immediate re-render so arrow labels reflect the new state on first click.
        st.rerun()


def _is_group_stage(r: dict) -> bool:
    # Records from full_bets_info contain group_name and stage in DEMO/real.
    return bool(r.get("group_name")) or str(r.get("stage") or "").upper() == "GROUP_STAGE"


def _is_knockout_stage(r: dict) -> bool:
    return str(r.get("stage") or "").upper() in KNOCKOUT_STAGES


def _match_number(r: dict) -> int:
    try:
        return int(r.get("match_number") or 0)
    except Exception:
        return 0


def _filter_matches(records: list[dict]) -> tuple[list[dict], dict]:
    """Return filtered records and UI meta.

    Filtering is based on stage toggles + match_number range.
    The slider min/max must adjust to the stage toggles.
    """

    # Stage toggles
    c1, c2 = st.columns([1, 1])
    with c1:
        only_groups = st.toggle("Tylko faza grupowa", value=False)
    with c2:
        only_knockout = st.toggle("Tylko faza pucharowa", value=False)

    stage_filtered = records
    if only_groups and not only_knockout:
        stage_filtered = [r for r in records if _is_group_stage(r)]
    elif only_knockout and not only_groups:
        stage_filtered = [r for r in records if _is_knockout_stage(r)]
    # If both toggles are on (or both off), treat as no stage restriction.

    nums = sorted({_match_number(r) for r in stage_filtered if _match_number(r) > 0})
    if not nums:
        return [], {"only_groups": only_groups, "only_knockout": only_knockout, "range": (0, 0)}

    min_n, max_n = nums[0], nums[-1]
    selected = st.slider(
        "Zakres meczów (nr)",
        min_value=min_n,
        max_value=max_n,
        value=(min_n, max_n),
        step=1,
    )

    lo, hi = selected
    final = [r for r in stage_filtered if lo <= _match_number(r) <= hi]

    meta = {"only_groups": only_groups, "only_knockout": only_knockout, "range": (lo, hi)}
    return final, meta


def build_table(records: list[dict]) -> dict:
    # per-user stats
    table = defaultdict(
        lambda: {
            "matches": 0,
            "points": 0.0,
            "buckets": {**{v: 0 for v in BUCKET_INT_VALUES}, BUCKET_HALF_KEY: 0},
            "_per_match": [],  # list of (match_number, points)
            "_form_history": [], # form (all matches)
        }
    )

    for r in records:
        # Only consider finished matches (not live)
        if classify_match_state(r) != "FINISHED":
            continue

        user = r["username"]
        mn = _match_number(r)

        # If no bet, just append the form history
        if r.get("home_bet") is None or r.get("away_bet") is None:
            table[user]["_form_history"].append((mn, None))
            continue

        pts_raw = r.get("points")
        pts = float(pts_raw) if pts_raw is not None else 0.0

        table[user]["matches"] += 1
        table[user]["points"] += pts
        table[user]["_per_match"].append((mn, pts))
        table[user]["_form_history"].append((mn, pts))

        # bucket counts
        # Points are guaranteed to be integers or integer + 0.5
        # - integer N -> bucket N (if in 1..5)
        # - N+0.5 -> bucket floor(N+0.5) and +0.5
        # - 0.5 -> +0.5 only (no zero column)
        whole = int(pts)
        is_half = abs(pts - (whole + 0.5)) < 1e-9 or abs(pts - 0.5) < 1e-9

        if whole in BUCKET_INT_VALUES:
            table[user]["buckets"][whole] += 1
        if is_half:
            table[user]["buckets"][BUCKET_HALF_KEY] += 1

    # finalize form (last 5 finished matches)
    for u, s in table.items():
        s["_form_history"].sort(key=lambda x: x[0])
        s["form"] = [pts for _, pts in s["_form_history"][-5:]]

    return dict(table)


def _color_from_style(style: str) -> str:
    # get_points_style returns e.g. 'color:#00c853;font-weight:600;'
    if not style:
        return "#808080"
    for token in style.split(';'):
        token = token.strip()
        if token.startswith('color:'):
            return token.split(':', 1)[1].strip() or "#808080"
    return "#808080"


def _form_dots_html(form_points: list[float | None]) -> str:
    dots = []
    for p in form_points:
        if p is None:
            col = "#555555"   # brak typu
        else:
            col = _color_from_style(get_points_style(p))

        dots.append(
            f"<span style='display:inline-block;width:7px;height:7px;border-radius:50%;background:{col};margin-left:3px;'></span>"
        )

    return "".join(dots)

def render_table():
    st.title("📋 Tabela")
    # Keep table sort arrow buttons compact (scope by button key prefix).
    # We avoid global `div.stButton > button` styling to not affect other pages.
    st.markdown(
        """
        <style>
        /* Target only our 3 table sort buttons by their Streamlit element key */
        div[data-testid="stButton"][data-key^="table_sort_toggle_"] > button {
            padding: 0.15rem 0.35rem;
            line-height: 1.0;
            min-height: 1.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    records = get_full_bets_info()

    # UI FILTERS (stage + match range)
    records, _meta = _filter_matches(records)

    table = build_table(records)

    if not table:
        st.info("Brak danych")
        return
    # SORTING STATE (controlled by header buttons)
    _ensure_sort_state()

    sort_key = st.session_state.get("table_sort_key", "points")
    sort_dir = st.session_state.get("table_sort_dir", "desc")

    def _sort_key(item):
        _user, s = item
        matches = float(s.get("matches") or 0)
        points = float(s.get("points") or 0)
        avg = (points / matches) if matches else 0.0

        if sort_key == "matches":
            return matches
        if sort_key == "avg":
            return avg
        # default: total points
        return points

    sorted_users = sorted(
        table.items(),
        key=_sort_key,
        reverse=(sort_dir == "desc"),
    )

    # Bucket column widths: keep integer buckets compact, give +½ a bit more room.
    bucket_widths = [0.45] * len(BUCKET_INT_VALUES) + [0.55]

    # SORT BUTTONS ROW (above header)
    btn_cols = st.columns([0.6, 2.2, 1.0] + bucket_widths + [1.0, 1.0, 1.6])

    # empty placeholders for # and Gracz
    with btn_cols[0]:
        st.markdown("")
    with btn_cols[1]:
        st.markdown("")

    with btn_cols[2]:
        _sort_toggle_button('matches')

    # no bucket sorting buttons
    for j in range((len(BUCKET_INT_VALUES) + 1)):
        with btn_cols[3 + j]:
            st.markdown("")

    with btn_cols[3 + (len(BUCKET_INT_VALUES) + 1)]:
        _sort_toggle_button('points')

    with btn_cols[4 + (len(BUCKET_INT_VALUES) + 1)]:
        _sort_toggle_button('avg')

    with btn_cols[5 + (len(BUCKET_INT_VALUES) + 1)]:
        st.markdown("")

    # HEADER (Streamlit columns)
    # Use the same layout engine as the sort buttons row to improve horizontal alignment.
    hdr_cols = st.columns([0.6, 2.2, 1.0] + bucket_widths + [1.0, 1.0, 1.6])

    with hdr_cols[0]:
        st.markdown("<div style='font-weight:600;opacity:0.7;font-size:13px;'>#</div>", unsafe_allow_html=True)
    with hdr_cols[1]:
        st.markdown("<div style='font-weight:600;opacity:0.7;font-size:13px;'>Gracz</div>", unsafe_allow_html=True)
    with hdr_cols[2]:
        st.markdown("<div style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>Zakłady</div>", unsafe_allow_html=True)

    for j, v in enumerate(BUCKET_INT_VALUES):
        with hdr_cols[3 + j]:
            st.markdown(f"<div style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>{v}</div>", unsafe_allow_html=True)

    # +0.5 column
    with hdr_cols[3 + len(BUCKET_INT_VALUES)]:
        st.markdown("<div style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>+½</div>", unsafe_allow_html=True)

    with hdr_cols[3 + (len(BUCKET_INT_VALUES) + 1)]:
        st.markdown("<div style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>Pkt</div>", unsafe_allow_html=True)
    with hdr_cols[4 + (len(BUCKET_INT_VALUES) + 1)]:
        st.markdown("<div style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>Pkt/Z</div>", unsafe_allow_html=True)
    with hdr_cols[5 + (len(BUCKET_INT_VALUES) + 1)]:
        st.markdown("<div style='font-weight:600;opacity:0.7;font-size:13px;text-align:center;'>Forma</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ROWS (ULTRA COMPACT)
    for i, (user, s) in enumerate(sorted_users, start=1):

        matches = s["matches"]
        points = s["points"]
        avg = points / matches if matches else 0

        form_html = _form_dots_html(s.get("form") or [])

        bucket_counts_int = [int((s.get('buckets') or {}).get(v, 0) or 0) for v in BUCKET_INT_VALUES]
        bucket_half = int((s.get('buckets') or {}).get(BUCKET_HALF_KEY, 0) or 0)
        row_cols = st.columns([0.6, 2.2, 1.0] + bucket_widths + [1.0, 1.0, 1.6])

        # #
        with row_cols[0]:
            st.markdown(f"<div style='font-size:14px;'>{i}</div>", unsafe_allow_html=True)

        # Gracz
        with row_cols[1]:
            st.markdown(f"<div style='font-size:14px;font-weight:500'>{format_username(user)}</div>", unsafe_allow_html=True)

        # Zakłady
        with row_cols[2]:
            st.markdown(f"<div style='font-size:14px;text-align:center;'>{matches}</div>", unsafe_allow_html=True)

        # Buckets 5..1
        for j, c in enumerate(bucket_counts_int):
            with row_cols[3 + j]:
                st.markdown(f"<div style='text-align:center;'><span style='font-size:11px;opacity:0.75;'>{c}</span></div>", unsafe_allow_html=True)

        # +0.5
        with row_cols[3 + len(BUCKET_INT_VALUES)]:
            st.markdown(f"<div style='text-align:center;'><span style='font-size:11px;opacity:0.75;'>{bucket_half}</span></div>", unsafe_allow_html=True)

        # Pkt
        with row_cols[4 + len(BUCKET_INT_VALUES)]:
            st.markdown(f"<div style='font-size:14px;text-align:center;font-weight:600'>{round(points,2)}</div>", unsafe_allow_html=True)

        # Pkt/Z
        with row_cols[5 + len(BUCKET_INT_VALUES)]:
            st.markdown(f"<div style='font-size:14px;text-align:center;'>{round(avg,4):.4f}</div>", unsafe_allow_html=True)

        # Forma
        with row_cols[6 + len(BUCKET_INT_VALUES)]:
            st.markdown(f"<div style='text-align:center;'>{form_html}</div>", unsafe_allow_html=True)
