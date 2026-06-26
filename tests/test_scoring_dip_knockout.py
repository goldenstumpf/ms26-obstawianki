from decimal import Decimal

from app.services.score_bets import calculate_points


def _mk_match(
    *,
    stage: str = "LAST_16",
    home_code: str = "HOME",
    away_code: str = "AWAY",
    flt_home: int,
    flt_away: int,
    duration: str = "REGULAR",
    pens_home: int | None = None,
    pens_away: int | None = None,
) -> dict:
    return {
        "stage": stage,
        "home_code": home_code,
        "away_code": away_code,
        "flt_home": flt_home,
        "flt_away": flt_away,
        "duration": duration,
        "pens_home": pens_home,
        "pens_away": pens_away,
    }


def _mk_bet(*, home_bet: int, away_bet: int, dip: str | None = None) -> dict:
    return {"home_bet": home_bet, "away_bet": away_bet, "dip": dip}


def test_knockout_draw_bet_penalty_pick_resolves_rezultat_against_win_in_90() -> None:
    # bet: (2:2, karne: HOME); score (3:0, 90) -> 1 pt for rezultat (HOME won)
    match = _mk_match(flt_home=3, flt_away=0, duration="REGULAR")
    bet = _mk_bet(home_bet=2, away_bet=2, dip="karne: HOME")
    assert calculate_points(bet, match) == Decimal("1")


def test_knockout_draw_bet_goal_difference_awarded_on_draw_scoreline() -> None:
    # bet (2:2, karne: HOME); score (1:1, karne: AWAY) -> 2 pts for goal difference
    match = _mk_match(
        flt_home=1,
        flt_away=1,
        duration="PENALTY_SHOOTOUT",
        pens_home=3,
        pens_away=4,
    )
    bet = _mk_bet(home_bet=2, away_bet=2, dip="karne: HOME")
    assert calculate_points(bet, match) == Decimal("2")


def test_knockout_draw_bet_goal_difference_plus_dip_bonus_when_penalty_winner_matches() -> None:
    # bet (2:2, karne: HOME); score (1:1, karne: HOME) -> 3 pts (2 + DIP)
    match = _mk_match(
        flt_home=1,
        flt_away=1,
        duration="PENALTY_SHOOTOUT",
        pens_home=5,
        pens_away=4,
    )
    bet = _mk_bet(home_bet=2, away_bet=2, dip="karne HOME")
    assert calculate_points(bet, match) == Decimal("3")


def test_knockout_draw_bet_exact_score_awarded_even_if_penalty_pick_wrong() -> None:
    # bet(2:2, karne: HOME); score(2:2, karne: AWAY) -> 4 pts for exact score
    match = _mk_match(
        flt_home=2,
        flt_away=2,
        duration="PENALTY_SHOOTOUT",
        pens_home=4,
        pens_away=5,
    )
    bet = _mk_bet(home_bet=2, away_bet=2, dip="karne: HOME")
    assert calculate_points(bet, match) == Decimal("4")


def test_knockout_draw_bet_exact_score_plus_dip_when_penalty_pick_matches() -> None:
    # bet (2:2, karne: HOME), score(2:2, karne: HOME) -> 5 pts (4 + DIP)
    match = _mk_match(
        flt_home=2,
        flt_away=2,
        duration="PENALTY_SHOOTOUT",
        pens_home=5,
        pens_away=4,
    )
    bet = _mk_bet(home_bet=2, away_bet=2, dip="karne: HOME")
    assert calculate_points(bet, match) == Decimal("5")


def test_knockout_non_draw_bet_can_get_rezultat_against_penalty_resolved_winner() -> None:
    # bet(3:0, 90), score(2:2, karne: HOME) -> 1 pt for rezultat (HOME won)
    match = _mk_match(
        flt_home=2,
        flt_away=2,
        duration="PENALTY_SHOOTOUT",
        pens_home=4,
        pens_away=3,
    )
    bet = _mk_bet(home_bet=3, away_bet=0, dip="90")
    assert calculate_points(bet, match) == Decimal("1")
