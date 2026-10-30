from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL


database_url = DATABASE_URL


engine = create_engine(database_url)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_engine(*, echo: bool = False) -> Engine:
    return create_engine(database_url, echo=echo)


def get_session_factory(engine_instance: Engine | None = None):
    return sessionmaker(
        bind=engine_instance or engine,
        autoflush=False,
        autocommit=False,
    )


def init_db(engine_instance: Engine | None = None) -> None:
    Base.metadata.create_all(bind=engine_instance or engine)


# Re-export model for existing imports used across the codebase.
from repository.models import Ticker  # noqa: E402
