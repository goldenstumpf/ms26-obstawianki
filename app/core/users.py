import json
from pathlib import Path

USERS_FILE = Path("app/data/users.json")


def load_users():
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def authenticate(nick, pin):
    users = load_users()

    if nick in users and users[nick]["pin"] == pin:
        return True

    return False