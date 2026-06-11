import json
from pathlib import Path

BETS_FILE = Path("app/data/bets.json")


def load_bets():
    if not BETS_FILE.exists():
        return {}
    return json.loads(BETS_FILE.read_text(encoding="utf-8"))


def save_bets(bets):
    BETS_FILE.write_text(json.dumps(bets, indent=2), encoding="utf-8")

def get_user_bets(user):
    all_bets = load_bets()
    return all_bets.get(user, {})

def save_user_bets(user, new_bets):
    all_bets = load_bets()

    if user not in all_bets:
        all_bets[user] = {}

    for match_id, bet in new_bets.items():
        all_bets[user][str(match_id)] = {
            "home": int(bet["home"]),
            "away": int(bet["away"])
        }

    save_bets(all_bets)