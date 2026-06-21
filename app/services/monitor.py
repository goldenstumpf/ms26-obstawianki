import time
from datetime import datetime

from services.fetch_matches import run_fetch_matches
from services.score_bets import run_scoring
from core.db import get_supabase


CHECK_INTERVAL_ACTIVE = 60
CHECK_INTERVAL_IDLE = 900


def has_matches_to_monitor():

    res = (
        supabase.table("matches")
        .select("match_id")
        .eq("needs_monitoring", True)
        .limit(1)
        .execute()
    )

    return len(res.data or []) > 0


def run_monitor():

    print("🚀 WC26 Monitor started")

    while True:

        try:

            if has_matches_to_monitor():

                print(
                    f"[{datetime.utcnow()}] ⚽ Matches to monitor"
                )

                run_fetch_matches()
                run_score_bets()

                print(
                    f"[{datetime.utcnow()}] 😴 Sleep {CHECK_INTERVAL_ACTIVE}s"
                )

                time.sleep(CHECK_INTERVAL_ACTIVE)

            else:

                print(
                    f"[{datetime.utcnow()}] 💤 No matches to monitor"
                )

                print(
                    f"[{datetime.utcnow()}] 😴 Sleep {CHECK_INTERVAL_IDLE}s"
                )

                time.sleep(CHECK_INTERVAL_IDLE)

        except Exception as e:

            print(f"❌ Monitor error: {e}")

            time.sleep(60)


if __name__ == "__main__":
    run_monitor()