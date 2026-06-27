import streamlit as st


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
