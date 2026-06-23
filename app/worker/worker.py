import logging
import time

from datetime import datetime
from datetime import timezone
from datetime import timedelta

from app.services.fetch_matches import run_fetch_matches
from app.services.score_bets import run_scoring

from app.core.db import get_supabase

logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("hpack").setLevel(logging.WARNING)
logging.getLogger("supabase").setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


LIVE_STATUSES = {
    "IN_PLAY",
    "PAUSED",
    "EXTRA_TIME",
    "PENALTY_SHOOTOUT",
    "LIVE,"
}


# --------------------------------------------------
# MATCH HELPERS
# --------------------------------------------------

def get_live_matches():
    res = (
        get_supabase()
        .table("matches")
        .select("match_id,status")
        .in_("status", list(LIVE_STATUSES))
        .execute()
    )

    return res.data or []


def get_next_match():
    now = (datetime.now(timezone.utc) - timedelta(minutes=90)).isoformat()

    res = (
        get_supabase()
        .table("matches")
        .select("*")
        .gt("utc_date", now)
        .order("utc_date")
        .limit(1)
        .execute()
    )

    if not res.data:
        return None

    return res.data[0]


# --------------------------------------------------
# SCHEDULER
# --------------------------------------------------

def compute_sleep_seconds() -> int:
    """
    Decide when next refresh should happen.
    """

    live_matches = get_live_matches()

    if live_matches:
        logger.info(
            f"{len(live_matches)} live match(es) found -> next run in 60 sec"
        )
        return 60

    next_match = get_next_match()

    if not next_match:
        logger.info(
            "No future matches -> sleep 12h"
        )
        return 12 * 60 * 60

    kickoff = datetime.fromisoformat(
        next_match["utc_date"].replace("Z", "+00:00")
    )

    now = datetime.now(timezone.utc)

    delta = kickoff - now

    minutes = delta.total_seconds() / 60

    logger.info(
        f"Next match #{next_match['match_number']} "
        f"in {minutes:.1f} min"
    )

    # match starts soon
    if minutes <= 30:
        return 120

    # today
    if minutes <= 12 * 60:
        return 1800

    # far away
    return 21600


# --------------------------------------------------
# MONITOR
# --------------------------------------------------

def run_monitor():
    logger.info("=" * 60)
    logger.info("MONITOR START")

    matches = run_fetch_matches()

    logger.info(
        f"Fetched {len(matches)} matches"
    )

    scoring_result = run_scoring()

    logger.info(
        f"Scoring result: {scoring_result}"
    )

    logger.info("MONITOR END")


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

def main():

    logger.info("Worker started")

    while True:

        try:
            run_monitor()

        except Exception:
            logger.exception("Monitor failed")

            sleep_seconds = 300

            logger.info(
                f"Retry in {sleep_seconds} sec"
            )

            time.sleep(sleep_seconds)

            continue

        sleep_seconds = compute_sleep_seconds()

        logger.info(
            f"Sleeping for {sleep_seconds} sec"
        )

        time.sleep(sleep_seconds)


if __name__ == "__main__":
    main()