from datetime import datetime, timedelta, timezone

from app.data.matches import list_matches


def has_matches_to_monitor():
    matches = list_matches()

    now = datetime.now(timezone.utc)

    for m in matches:
        if m["status"] == "FINISHED":
            continue

        start = datetime.fromisoformat(m["utc_date"].replace("Z", "+00:00"))

        if start - now < timedelta(hours=1):
            return True

    return False


if __name__ == "__main__":
    print(has_matches_to_monitor())