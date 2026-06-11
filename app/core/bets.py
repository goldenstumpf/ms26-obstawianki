import json
from datetime import datetime
from pathlib import Path
import supabase


BETS_FILE = Path("app/data/bets.json")


def load_bets():
    if not BETS_FILE.exists():
        return {}
    return json.loads(BETS_FILE.read_text(encoding="utf-8"))


def save_bets(bets):
    BETS_FILE.write_text(json.dumps(bets, indent=2), encoding="utf-8")

def get_user_bets(user):
    res = supabase.table("bets").select("*").eq("user", user).execute()

    return {
        row["match_id"]: {
            "home": row["home"],
            "away": row["away"]
        }
        for row in res.data
    }

def save_user_bets(user, bets):
    for match_id, bet in bets.items():
        supabase.table("bets").upsert({
            "user": user,
            "match_id": str(match_id),
            "home": bet["home"],
            "away": bet["away"]
        }).execute()