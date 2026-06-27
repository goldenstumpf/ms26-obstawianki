from __future__ import annotations

import streamlit as st

from app.services.score_bets import calculate_points
from app.utils.components import render_match_row


def render_rules() -> None:
    st.title("📜 Reguły")

    st.markdown(
        """
## 1. Ogólne zasady
1. Zabawa polega na typowaniu wyników meczów turnieju oraz zbieraniu punktów za trafność typów.
2. Zwycięzcą zabawy zostaje uczestnik, który po zakończeniu turnieju zgromadzi największą liczbę punktów.

## 2. Zakłady
### 2.1. Mecze
1. Zabawa obejmuje mecze całego turnieju.
2. Możliwość wprowadzania zakładu dotyczy wyłącznie meczów:
   1) rozpoczynających się w najbliższych 72 godzinach, oraz
   2) dla których znane są obie drużyny (gospodarze i goście).

### 2.2. Zmiana zakładów
1. Dla jednego meczu dopuszcza się wprowadzenie zakładu oraz jego późniejszą zmianę.
2. Liczba zmian zakładu dla jednego meczu jest nieograniczona.
3. Zmiana zakładu jest dopuszczalna wyłącznie do oficjalnej godziny rozpoczęcia meczu.

### 2.3. Sytuacje nadzwyczajne
1. W wyjątkowych, nagłych przypadkach dopuszcza się przekazanie zakładu organizatorowi innym kanałem.
2. Warunkiem rozpatrzenia takiego typu jest udokumentowanie, że został on przekazany na czas.
3. O uwzględnieniu zakładu przekazanego w trybie nadzwyczajnym decyduje organizator.

## 3. Punktacja
### 3.1. Podstawowa
1. Za jeden mecz przyznaje się wyłącznie jeden z poniższych wyników punktowych (nie sumują się):
   1) **4 pkt** – za **dokładny wynik**,
   2) **2 pkt** – za **różnicę bramek**,
   3) **1 pkt** – za **rezultat**.
2. W meczach fazy grupowej rezultat obejmuje również remis.
3. W meczach pucharowych rezultat odnosi się do wskazania zwycięzcy; w przypadku zakładu remisowego wymagane jest wskazanie zwycięzcy w DIP (pkt 3.3).

### 3.2. Połówka pocieszenia
1. Dodatkowo przyznaje się **+0,5 pkt (połówka pocieszenia)**, jeżeli zakład różni się od wyniku końcowego łącznie o dokładnie jedną bramkę, tj. spełniony jest warunek:
   `|wynik gosp. - typ gosp.| + |wynik gość - typ gość| == 1`.

### 3.3. DIP (Dodatkowa Informacja Pucharowa)
1. DIP jest skrótem od **Dodatkowa Informacja Pucharowa** i dotyczy wyłącznie meczów pucharowych.
2. Jeżeli zakład wskazuje zwycięstwo jednej z drużyn (zakład nieremisowy), DIP dotyczy **czasu rozstrzygnięcia** i może przyjąć wartość:
   1) `90` – rozstrzygnięcie w regulaminowym czasie,
   2) `120` – rozstrzygnięcie po dogrywce.
3. Za prawidłowe wskazanie czasu rozstrzygnięcia przyznaje się **+1 pkt**, pod warunkiem że zakład uzyskał co najmniej **1 pkt punktów bazowych** (wskazano dobrego zwycięzcę).
4. Jeżeli zakład wskazuje remis, DIP służy do wskazania zwycięzcy w rzutach karnych w postaci: `karne: XXX`.
5. W meczach pucharowych wskazanie zwycięzcy w DIP (karne) może zostać uwzględnione przy rozstrzyganiu rezultatu (1 pkt), ponieważ w meczach pucharowych nie występuje remis jako wynik rozstrzygający.
6. Jeżeli mecz faktycznie został rozstrzygnięty w rzutach karnych, za prawidłowe wskazanie zwycięzcy w DIP przyznaje się dodatkowo **+1 pkt**.

## 4. Ranking
1. O miejscu w rankingu decydują kolejno:
   1) łączna liczba punktów,
   2) liczba meczów trafionych dokładnie (dokładny wynik),
   3) średnia punktów,
   4) remis.

## 5. Interpretacje
1. Całość niniejszego regulaminu podlega ostatecznej interpretacji organizatora.
"""
    )

    st.divider()
    st.subheader("🧮 Kalkulator punktów")

    mode = st.radio(
        "Tryb",
        options=["Faza grupowa", "Mecze pucharowe"],
        horizontal=True,
    )

    stage = "GROUP_STAGE" if mode == "Faza grupowa" else "LAST_16"

    def _sim_record(match_id: str, *, stage_value: str) -> dict:
        # Minimal fields required by render_match_row in edit mode.
        return {
            "match_id": match_id,
            "match_number": 0,
            "minute": None,
            "utc_date": "2099-01-01T00:00:00Z",
            "status": "SCHEDULED",
            "stage": stage_value,
            "group_name": "",
            "home_team": "Drużyna A",
            "away_team": "Drużyna B",
            "home_code": "A",
            "away_code": "B",
            "home_crest": None,
            "away_crest": None,
            # bet fields (optional)
            "home_bet": None,
            "away_bet": None,
            "dip": None,
        }

    r_bet = _sim_record("rules_sim_bet", stage_value=stage)
    r_actual = _sim_record("rules_sim_actual", stage_value=stage)

    st.markdown("### Zakład")
    render_match_row(r_bet, mode="edit")

    st.markdown("### Rzeczywisty wynik")
    render_match_row(r_actual, mode="edit")

    # -------------------------
    # CALCULATE (below components)
    # -------------------------
    bet_mid = str(r_bet["match_id"])
    act_mid = str(r_actual["match_id"])

    bet = {
        "home_bet": st.session_state.get(f"home_{bet_mid}"),
        "away_bet": st.session_state.get(f"away_{bet_mid}"),
        "dip": st.session_state.get(f"dip_{bet_mid}"),
    }

    actual_home = st.session_state.get(f"home_{act_mid}")
    actual_away = st.session_state.get(f"away_{act_mid}")
    actual_dip = st.session_state.get(f"dip_{act_mid}")

    # Build a match dict compatible with calculate_points
    match: dict = {
        "stage": stage,
        "home_code": "A",
        "away_code": "B",
        "flt_home": actual_home,
        "flt_away": actual_away,
        "duration": None,
        "pens_home": None,
        "pens_away": None,
    }

    # Translate the *actual* DIP selection into duration + penalty winner
    if stage != "GROUP_STAGE" and actual_home is not None and actual_away is not None:
        if isinstance(actual_dip, str) and actual_dip.strip().startswith("karne"):
            match["duration"] = "PENALTY_SHOOTOUT"
            # Set a minimal penalty score so winner is unambiguous.
            if "A" in actual_dip:
                match["pens_home"] = 1
                match["pens_away"] = 0
            else:
                match["pens_home"] = 0
                match["pens_away"] = 1
        elif str(actual_dip).strip() == "120":
            match["duration"] = "EXTRA_TIME"
        elif str(actual_dip).strip() == "90":
            match["duration"] = "REGULAR"

    points = calculate_points(bet=bet, match=match)

    # Breakdown (mirrors calculate_points semantics)
    breakdown = {"bazowe": None, "połówka pocieszenia": None, "DIP": None}

    if match.get("flt_home") is None or match.get("flt_away") is None:
        breakdown["bazowe"] = None
        breakdown["połówka pocieszenia"] = None
        breakdown["DIP"] = None
    elif bet.get("home_bet") is None or bet.get("away_bet") is None:
        breakdown["bazowe"] = None
        breakdown["połówka pocieszenia"] = None
        breakdown["DIP"] = None
    else:
        mh = int(match["flt_home"])
        ma = int(match["flt_away"])
        bh = int(bet["home_bet"])
        ba = int(bet["away_bet"])

        # base
        base = 0
        if bh == mh and ba == ma:
            base = 4
        elif (bh - ba) == (mh - ma):
            base = 2
        else:
            if stage == "GROUP_STAGE":
                base = 1 if ((bh > ba) - (bh < ba)) == ((mh > ma) - (mh < ma)) else 0
            else:
                # winner-based result; resolve actual winner from penalties if present
                if match.get("duration") == "PENALTY_SHOOTOUT":
                    winner = "A" if (match.get("pens_home") or 0) > (match.get("pens_away") or 0) else "B"
                else:
                    winner = "A" if mh > ma else ("B" if ma > mh else None)

                bet_winner = "A" if bh > ba else ("B" if ba > bh else None)
                if bet_winner is None:
                    dip = str(bet.get("dip") or "")
                    bet_winner = "A" if "A" in dip else ("B" if "B" in dip else None)

                base = 1 if (winner and bet_winner and winner == bet_winner) else 0

        half = 0.5 if abs(mh - bh) + abs(ma - ba) == 1 else 0.0

        dip_bonus = 0.0
        if stage != "GROUP_STAGE":
            d = bet.get("dip")
            d_str = str(d or "").strip()
            if d_str.startswith("karne"):
                if match.get("duration") == "PENALTY_SHOOTOUT":
                    winner = "A" if (match.get("pens_home") or 0) > (match.get("pens_away") or 0) else "B"
                    if (winner == "A" and "A" in d_str) or (winner == "B" and "B" in d_str):
                        dip_bonus = 1.0
            else:
                if base >= 1 and d_str in {"90", "120"}:
                    if (d_str == "90" and match.get("duration") == "REGULAR") or (
                        d_str == "120" and match.get("duration") == "EXTRA_TIME"
                    ):
                        dip_bonus = 1.0

        breakdown["bazowe"] = base
        breakdown["połówka pocieszenia"] = half
        breakdown["DIP"] = dip_bonus

    st.markdown("#### Wynik punktowy")

    if points is None:
        st.info("Uzupełnij oba wyniki (Zakład i Rzeczywisty wynik), aby zobaczyć punkty.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Razem", f"{float(points):g} pkt")
        c2.metric("Bazowe", f"{breakdown['bazowe']}")
        c3.metric("Połówka", f"{breakdown['połówka pocieszenia']}")
        c4.metric("DIP", f"{breakdown['DIP']}")
