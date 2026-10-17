import logging
from collections.abc import Sequence

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session as OrmSession

from src.app.api.v1.genre.model import GenreModel as Genre
from src.app.api.v1.genre.schema import (
    GenreBase,
    GenreCreate,
    GenreDelete,
    GenreUpdate,
)
from src.app.api.v1.track.schema import TrackCreate
from src.app.core.logging import Loggers
from src.app.services.operators.database import DatabaseOperator

logger = logging.getLogger(Loggers.DB)


class GenreService(DatabaseOperator):
    def __init__(self, session: OrmSession):
        self._db = session

    def create_genre(self, entry: GenreCreate):
        logger.debug("Creating Genre entries...")

        with self._db.begin():
            stmt = insert(Genre).values(name=entry.name).returning(Genre)
            result = self._db.scalars(stmt).one()  # pyright: ignore [reportCallIssue, reportArgumentType]

        logger.debug("Created Genre entry")
        return result

    def create_genre_from_track(self, track: TrackCreate) -> Sequence[Genre]:
        logger.debug("Creating Genre(s) from Track entry...")

        instances = []

        with self._db.begin():
            select_stmt = select(Genre).where(Genre.name.in_(track.genres))
            results = self._db.scalars(select_stmt).all()
            present_genres: set[str] = {g.name for g in results}
            # stores current GenreModel objects...
            instances.extend(results)

        extra_genres = [
            Genre(name=genre)
            for genre in track.genres
            if genre not in present_genres
        ]

        if extra_genres:
            # ...and creates new ones for those not present
            instances.extend(extra_genres)

            with self._db.begin():
                self._db.add_all(instances)

        # remove from current session to add to a new one later
        for instance in instances:
            self._db.expunge(instance)

        return instances

    def read_all(self) -> Sequence[Genre]:
        logger.debug("Reading all genre entries...")

        stmt = select(Genre)
        return self._db.scalars(stmt).all()

    def read_genre(self, entry: GenreBase):
        stmt = select(Genre).where(Genre.id == entry.id)
        return self._db.scalars(stmt).one()

    def update_genre(self, entry: GenreUpdate):
        logger.debug("Updating one genre entry...")

        with self._db.begin():
            genre_to_be_updated = entry.model_dump(exclude_unset=True)
            stmt = (
                update(Genre)
                .where(Genre.id == entry.id)
                .values(**genre_to_be_updated)
                .returning(Genre)
            )
            result = self._db.scalars(stmt).one()

        return result

    def delete_all(self):
        logger.debug("Deleting all entries from Genre table...")

        with self._db.begin():
            stmt = delete(Genre)
            num_deleted_rows = self._db.execute(stmt).rowcount  # pyright: ignore [reportAttributeAccessIssue]

            if not num_deleted_rows:
                error_msg = "Delete failed. Database is empty."
                logger.exception(error_msg)
                raise HTTPException(
                    detail=error_msg,
                    status_code=http_status.HTTP_404_NOT_FOUND,
                )

        logger.debug(f"Deleted {num_deleted_rows} row(s) from Genre table")

    def delete_genre(self, entry: GenreDelete) -> None:
        with self._db.begin():
            stmt = delete(Genre).where(Genre.id == entry.id)
            num_deleted_rows = self._db.execute(stmt).rowcount  # pyright: ignore [reportAttributeAccessIssue]

            if not num_deleted_rows:
                error_msg = "Delete failed. Database is empty."
                logger.exception(error_msg)
                raise HTTPException(
                    detail=error_msg,
                    status_code=http_status.HTTP_404_NOT_FOUND,
                )

        logger.debug(f"Deleted entry {entry.id} from Genre table")
