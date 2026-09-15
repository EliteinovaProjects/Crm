from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


def _normalize_database_url(url: str) -> str:
    """Normalize a database URL for serverless deployment.

    - Some providers (Heroku, older tooling) emit ``postgres://`` which
      SQLAlchemy 2.x no longer understands - map it to ``postgresql://``.
    - Ensure the Neon connection string enforces SSL when it is not stated
      explicitly. Neon *requires* SSL, and its pooled endpoint may include
      ``channel_binding=require``.
    """
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    if url.startswith("postgresql://") and "sslmode=" not in url:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}sslmode=require"

    return url


DATABASE_URL = _normalize_database_url(settings.DATABASE_URL)

# ``pool_pre_ping`` + ``pool_recycle`` make the engine resilient to the
# dropped/idle connections that are common on serverless platforms
# (Vercel) talking to a Neon Postgres instance.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()