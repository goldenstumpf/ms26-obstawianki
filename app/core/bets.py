import json
from pathlib import Path

BETS_FILE = Path("app/data/bets.json")


def load_bets():
    if not BETS_FILE.exists():
        return {}
    return json.loads(BETS_FILE.read_text(encoding="utf-8"))


def save_bets(bets):
    BETS_FILE.write_text(json.dumps(bets, indent=2), encoding="utf-8")


def save_user_bets(user, predictions):
    bets = load_bets()

    if user not in bets:
        bets[user] = {}

    for match_id, bet in predictions.items():
        bets[user][str(match_id)] = bet

    save_bets(bets)