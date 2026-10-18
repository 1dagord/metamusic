import logging

import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from src.app.core.logging import Loggers
from src.app.db.base import Base
from src.app.db.config import get_db_session
from src.app.main import app

logger = logging.getLogger(Loggers.TEST_DB)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
  DATABASE_URL,
  connect_args={"check_same_thread": False},
  poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine,
)

Base.metadata.create_all(engine)


@pytest.fixture(scope="session")
def override_get_db_session():
  logger.debug("Overriding get_database(...) for testing...")

  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()


app.dependency_overrides[get_db_session] = override_get_db_session
