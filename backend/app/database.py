from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def ensure_sslmode(url: str) -> str:
    if not url:
        return url

    parsed = urlparse(url)

    if parsed.scheme and parsed.scheme.startswith("postgres"):
        qs = parse_qs(parsed.query)

        if "sslmode" not in qs:
            qs["sslmode"] = ["require"]
            parsed = parsed._replace(
                query=urlencode(qs, doseq=True)
            )
            return urlunparse(parsed)

    return url


def create_engine_with_test(url):
    engine = create_engine(url)

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("[INFO] Successfully connected to database")
    return engine


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

normalized = ensure_sslmode(DATABASE_URL)

try:
    engine = create_engine_with_test(normalized)
except Exception as exc:
    raise RuntimeError(f"Could not connect to database: {exc}") from exc

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()