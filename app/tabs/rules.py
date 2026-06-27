from __future__ import annotations

import streamlit as st

from app.services.score_bets import calculate_points
from app.utils.components import render_match_row


def render_rules() -> None:
    st.title("📜 Reguły")

    st.markdown(
        """
## 1. Postanowienia ogólne

1. Zabawa polega na typowaniu wyników meczów objętych turniejem oraz zdobywaniu punktów za poprawność typów.
2. Zwycięzcą zostaje uczestnik, który po zakończeniu turnieju zgromadzi największą liczbę punktów.
3. Regulamin określa zasady wprowadzania typów, przyznawania punktów oraz ustalania klasyfikacji końcowej.

## 2. Zakres zabawy

### 2.1. Mecze objęte typowaniem

1. Typowanie obejmuje wszystkie mecze rozgrywane w ramach turnieju.
2. Typ można wprowadzić wyłącznie dla meczu, który spełnia łącznie następujące warunki:
   1) jego rozpoczęcie nastąpi w ciągu najbliższych 72 godzin,
   2) znane są obie drużyny uczestniczące w meczu.

### 2.2. Wprowadzanie i zmiana typów

1. Dla każdego meczu uczestnik może wprowadzić jeden typ.
2. Wprowadzony typ może być dowolnie zmieniany przed rozpoczęciem meczu.
3. Liczba zmian typu przed rozpoczęciem meczu jest nieograniczona.
4. Po oficjalnej godzinie rozpoczęcia meczu typ nie może zostać dodany ani zmieniony.

### 2.3. Sytuacje nadzwyczajne

1. W wyjątkowych i nagłych przypadkach uczestnik może przekazać typ organizatorowi innym kanałem niż standardowy sposób wprowadzania typów.
2. Warunkiem uwzględnienia takiego typu jest możliwość potwierdzenia, że został on przekazany przed rozpoczęciem meczu.
3. Uwzględnienie typu przekazanego w trybie nadzwyczajnym ma charakter wyjątkowy i każdorazowo wymaga decyzji organizatora.

## 3. Zasady punktacji

### 3.1. Punktacja podstawowa

1. Za każdy mecz uczestnik może otrzymać punkty bazowe wyłącznie z jednego z poniższych tytułów:
   1) **4 punkty** – za trafienie dokładnego wyniku meczu,
   2) **2 punkty** – za trafienie różnicy bramek,
   3) **1 punkt** – za trafienie rezultatu meczu.
2. Punkty bazowe za jeden mecz nie sumują się.
3. Przez **dokładny wynik** rozumie się prawidłowe wskazanie liczby bramek zdobytych przez każdą z drużyn.
4. Przez **różnicę bramek** rozumie się prawidłowe wskazanie różnicy między liczbą bramek obu drużyn, bez konieczności trafienia dokładnego wyniku.
5. Przez **rezultat meczu** rozumie się:
   1) w meczach fazy grupowej – prawidłowe wskazanie zwycięstwa jednej lub drugiej drużyny, albo remisu,
   2) w meczach fazy pucharowej – prawidłowe wskazanie zwycięstwa jednej lub drugiej drużyny, z uwzględnieniem zasad określonych w pkt 3.3-3.4.

### 3.2. Połówka pocieszenia

1. Uczestnik może otrzymać dodatkowo **0,5 punktu**, jeżeli jego typ różni się od rzeczywistego wyniku łącznie o dokładnie jedną bramkę.
2. Warunek jest spełniony, gdy:

   `|wynik gospodarzy - typ gospodarzy| + |wynik gości - typ gości| = 1`

3. Połówka pocieszenia sumuje się z punktacją bazową.

### 3.3. DIP

1. **DIP (Dodatkowa Informacja Pucharowa)** dotyczy wyłącznie meczów fazy pucharowej. I występuje w dwóch odmianach.
   1) **DIP (czas)**, jeżeli podstawowy typ wskazuje zwycięstwo jednej z drużyn,
   2) **DIP (karne)**, jeżeli podstawowy typ wskazuje remis.
2. Brak wymaganego DIP w meczu fazy pucharowej może skutkować nieuwzględnieniem części punktacji zależnej od tego wskazania.
3. DIP nie ma zastosowania do meczów fazy grupowej.

**DIP (czas) – czas rozstrzygnięcia**

4. W przypadku obstawienia zwycięstwa którejś z drużyn w fazie pucharowej, uczestnik zobowiązany jest do wskazania czasu rozstrzygnięcia spotkania.
5. DIP (czas) może przyjąć jedną z następujących wartości:
   1) **`90`** – jeżeli mecz ma zostać rozstrzygnięty w regulaminowym czasie gry,
   2) **`120`** – jeżeli mecz ma zostać rozstrzygnięty po dogrywce.
6. Za prawidłowe wskazanie DIP (czas) przyznaje się **+1 punkt**, pod warunkiem że uczestnik uzyskał za dany mecz co najmniej **1 punkt bazowy** (czyli tylko jeśli poprawnie wskazał co najmniej rezultat meczu).

**DIP (karne) – zwycięzca karnych**

7. W przypadku typu remisowego w fazie pucharowej, uczestnik jest zobowiązany do wskazania zwycięzcy serii rzutów karnych w formie:

   `karne: [nazwa drużyny]`

8. W przypadku typu remisowego w meczu fazy pucharowej wskazanie zwycięzcy w karnych jest uwzględniane przy ocenie trafienia rezultatu meczu, ponieważ w fazie pucharowej remis nie stanowi wyniku ostatecznie rozstrzygającego.
9. Jeżeli mecz został rozstrzygnięty w serii rzutów karnych, za prawidłowe wskazanie zwycięzcy w DIP (karne) przyznaje się **+1 punkt**.

## 4. Klasyfikacja

1. O miejscu uczestnika w klasyfikacji końcowej decydują kolejno:
   1) łączna liczba zdobytych punktów,
   2) liczba meczów z trafionym dokładnym wynikiem,
   3) średnia liczba punktów na obstawiony mecz.
2. Jeżeli zastosowanie wszystkich kryteriów wskazanych w ust. 1 nie pozwoli na ustalenie kolejności, uczestnicy zajmują to samo miejsce w klasyfikacji.

## 5. Postanowienia końcowe

1. Organizator zastrzega sobie prawo do rozstrzygania sytuacji nieuregulowanych w niniejszym regulaminie.
2. Ostateczna interpretacja postanowień regulaminu należy do organizatora.
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
