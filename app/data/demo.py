import os


def demo_mode_enabled() -> bool:
    """Return True when DEMO_MODE is enabled.

    DEMO_MODE is intended for local development (e.g., corporate laptops with SSL
    interception) to run the UI without any Supabase network calls.
    """

    return os.getenv("DEMO_MODE", "0") in {"1", "true", "TRUE", "yes", "YES"}
