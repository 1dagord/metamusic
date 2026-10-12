import logging
from collections.abc import Sequence

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session as OrmSession

from src.api.v1.genre.model import GenreModel as Genre
from src.api.v1.genre.schema import GenreCreate
from src.core.logging import Loggers
from src.services.operators.database import DatabaseOperator

logger = logging.getLogger(Loggers.DB)


class GenreService(DatabaseOperator):
    def __init__(self, session: OrmSession):
        self._db = session

    def create_genre(self, entries: Sequence[GenreCreate]) -> None:
        instances = [
            Genre(
                name=entry.name,
            )
            for entry in entries
        ]

        with self._db.begin():
            self._db.add_all(instances)

    def read_all(self) -> Sequence[Genre]:
        logger.debug("Reading all genre entries...")

        stmt = select(Genre)
        return self._db.scalars(stmt).all()

    def delete_all(self):
        logger.debug("Deleting all entries from Genre table...")

        with self._db.begin():
            stmt = delete(Genre)
            num_deleted_rows = self._db.execute(stmt).rowcount

            if not num_deleted_rows:
                error_msg = "Database is empty"

                logger.exception(error_msg)

                raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND)

        logger.debug(f"Deleted {num_deleted_rows} from Genre table")
