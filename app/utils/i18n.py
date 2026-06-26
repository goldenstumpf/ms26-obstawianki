"""Polish translations / labels.

This module contains simple mapping helpers used by Streamlit UI rendering.
"""

from __future__ import annotations

COUNTRIES = {
    # Grupa A
    "Mexico": "Meksyk",
    "South Africa": "Republika Południowej Afryki",
    "South Korea": "Korea Południowa",
    "Czechia": "Czechy",
    # Grupa B
    "Canada": "Kanada",
    "Bosnia-Herzegovina": "Bośnia i Hercegowina",
    "Qatar": "Katar",
    "Switzerland": "Szwajcaria",
    # Grupa C
    "Brazil": "Brazylia",
    "Morocco": "Maroko",
    "Haiti": "Haiti",
    "Scotland": "Szkocja",
    # Grupa D
    "United States": "Stany Zjednoczone",
    "Paraguay": "Paragwaj",
    "Australia": "Australia",
    "Turkey": "Turcja",
    # Grupa E
    "Germany": "Niemcy",
    "Curaçao": "Curaçao",
    "Ivory Coast": "Wybrzeże Kości Słoniowej",
    "Ecuador": "Ekwador",
    # Grupa F
    "Netherlands": "Holandia",
    "Japan": "Japonia",
    "Tunisia": "Tunezja",
    "Sweden": "Szwecja",
    # Grupa G
    "Belgium": "Belgia",
    "Egypt": "Egipt",
    "Iran": "Iran",
    "New Zealand": "Nowa Zelandia",
    # Grupa H
    "Spain": "Hiszpania",
    "Cape Verde Islands": "Wyspy Zielonego Przylądka",
    "Saudi Arabia": "Arabia Saudyjska",
    "Uruguay": "Urugwaj",
    # Grupa I
    "France": "Francja",
    "Senegal": "Senegal",
    "Iraq": "Irak",
    "Norway": "Norwegia",
    # Grupa J
    "Argentina": "Argentyna",
    "Algeria": "Algieria",
    "Austria": "Austria",
    "Jordan": "Jordania",
    # Grupa K
    "Portugal": "Portugalia",
    "Congo DR": "Demokratyczna Republika Kongo",
    "Uzbekistan": "Uzbekistan",
    "Colombia": "Kolumbia",
    # Grupa L
    "England": "Anglia",
    "Croatia": "Chorwacja",
    "Ghana": "Ghana",
    "Panama": "Panama",
}

STAGES = {
    "GROUP_STAGE": "Faza grupowa",
    "LAST_32": "1/16 finału",
    "LAST_16": "1/8 finału",
    "QUARTER_FINALS": "Ćwierćfinał",
    "SEMI_FINALS": "Półfinał",
    "THIRD_PLACE": "Mecz o 3. miejsce",
    "FINAL": "Finał",
}

GROUPS = {
    "GROUP_A": "Grupa A",
    "GROUP_B": "Grupa B",
    "GROUP_C": "Grupa C",
    "GROUP_D": "Grupa D",
    "GROUP_E": "Grupa E",
    "GROUP_F": "Grupa F",
    "GROUP_G": "Grupa G",
    "GROUP_H": "Grupa H",
    "GROUP_I": "Grupa I",
    "GROUP_J": "Grupa J",
    "GROUP_K": "Grupa K",
    "GROUP_L": "Grupa L",
}


def country(name: str) -> str:
    return COUNTRIES.get(name, name)


def stage(name: str | None) -> str:
    if not name:
        return ""
    return STAGES.get(name, name)


def group(name: str | None) -> str:
    if not name:
        return ""
    return GROUPS.get(name, name)
