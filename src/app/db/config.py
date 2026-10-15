import logging
from collections.abc import Generator

from sqlalchemy import Engine, create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.orm import close_all_sessions, sessionmaker

from src.app.api.v1.artist.model import ArtistModel
from src.app.api.v1.genre.model import GenreModel
from src.app.api.v1.track.model import TrackModel
from src.app.core.config import config
from src.app.core.logging import Loggers
from src.app.db.associations import (
    ArtistTrackAssociation,
    GenreTrackAssociation,
)
from src.app.db.base import Base

logger = logging.getLogger(Loggers.DB)

DATABASE_MODELS = [
    TrackModel,
    GenreModel,
    ArtistModel,
    ArtistTrackAssociation,
    GenreTrackAssociation,
]


def create_sqlite_database_engine() -> Engine:
    try:
        engine = create_engine(config.sqlite_db_url)

    except SQLAlchemyError:
        error_msg = "Failed to configure the database"
        logger.exception(error_msg)
        raise

    logger.debug(
        "SQLite database engine created. Waiting for session creation..."
    )

    return engine


def initialize_database(engine: Engine) -> None:
    try:
        Base.metadata.create_all(engine)

        created_tables: set[str] = set(inspect(engine).get_table_names())
        expected_tables: set[str] = {
            model.__tablename__ for model in DATABASE_MODELS
        }
        missing_tables: set[str] = created_tables - expected_tables

        logger.debug(
            f"Created/found the following database tables: {created_tables}"
        )

        if missing_tables:
            raise RuntimeError(
                f"Database initialization did not create the following tables: {missing_tables}"
            )

        logger.debug("Database initialization successful! Ready for use")

    except Exception as e:
        logger.exception(
            f"Database initialization failed with exception type {type(e).__name__}"
        )
        raise


def get_db_session() -> Generator[OrmSession]:
    print("--- Getting database... ---")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def teardown_database(engine: Engine) -> None:
    close_all_sessions()
    engine.dispose()


engine = create_sqlite_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger.debug("Database session created. Waiting for initialization...")
