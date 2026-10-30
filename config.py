import os
from dotenv import load_dotenv

load_dotenv()


def normalize_database_url(raw_url: str | None) -> str | None:
    if raw_url is None:
        return None

    # psycopg2 rejects '?schema=public' in the DSN string.
    # Strip it so the URL remains valid while still using the default public schema.
    if "?schema=" in raw_url:
        return raw_url.split("?schema=", 1)[0]
    return raw_url


IBKR_HOST = os.getenv("IBKR_HOST", "127.0.0.1")
IBKR_PORT = int(os.getenv("IBKR_PORT", "4002"))
IBKR_CLIENT_ID = int(os.getenv("IBKR_CLIENT_ID", "1"))
DATABASE_URL = normalize_database_url(os.getenv("DATABASE_URL"))