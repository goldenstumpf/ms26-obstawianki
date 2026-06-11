import os
import requests
import json
from datetime import datetime

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://api.football-data.org/v4"

def fetch_matches(competition_id=2000):
    """
    Pobiera mecze dla danej ligi (domyślnie dla Mistrzostw Świata) korzystając z football-data.org.
    """

    url = f"{BASE_URL}/competitions/{competition_id}/matches"

    headers = {
        "X-Auth-Token": API_KEY
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status

    data = response.json()

    matches = data.get("matches", [])

    matches.sort(key=lambda m: m["utcDate"])

    for i, match in enumerate(matches, start=1):
        match["matchNumber"] = i

    return matches

def save_matches_to_json(matches, path="app/data/matches.json"):
    """
    Zapisuje mecze do JSON
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=True, indent=2)

if __name__ == "__main__":
    matches = fetch_matches()

    save_matches_to_json(matches)

    print(f"Zapisano {len(matches)} meczów do JSON")