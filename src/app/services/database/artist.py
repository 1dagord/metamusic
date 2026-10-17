import logging
from collections.abc import Sequence

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session as OrmSession

from src.app.api.v1.artist.model import ArtistModel as Artist
from src.app.api.v1.artist.schema import (
    ArtistBase,
    ArtistCreate,
    ArtistDelete,
    ArtistUpdate,
)
from src.app.api.v1.track.schema import TrackCreate
from src.app.core.logging import Loggers
from src.app.services.operators.database import DatabaseOperator

logger = logging.getLogger(Loggers.DB)


class ArtistService(DatabaseOperator):
    def __init__(self, session: OrmSession):
        self._db = session

    def create_artist(self, entry: ArtistCreate) -> Artist:
        logger.debug("Creating Artist entry...")

        with self._db.begin():
            stmt = insert(Artist).values(name=entry.name).returning(Artist)
            result = self._db.scalars(stmt).one()  # pyright: ignore [reportCallIssue, reportArgumentType]

        logger.debug("Created Artist entry")
        return result

    def create_artist_from_track(self, track: TrackCreate) -> Sequence[Artist]:
        logger.debug("Creating Artist(s) from Track entry...")

        instances = []

        with self._db.begin():
            select_stmt = select(Artist).where(Artist.name.in_(track.artists))
            results = self._db.scalars(select_stmt).all()
            present_artists: set[str] = {a.name for a in results}
            # stores current ArtistModel objects...
            instances.extend(results)

        extra_artists = [
            Artist(name=artist)
            for artist in track.artists
            if artist not in present_artists
        ]

        if extra_artists:
            # ...and creates new ones for those not present
            instances.extend(extra_artists)

            with self._db.begin():
                self._db.add_all(instances)

        # remove from current session to add to a new one later
        for instance in instances:
            self._db.expunge(instance)

        return instances

    def read_artist(self, entry: ArtistBase) -> Artist:
        stmt = select(Artist).where(Artist.id == entry.id)
        return self._db.scalars(stmt).one()

    def read_all(self) -> Sequence[Artist]:
        logger.debug("Reading all artist entries...")

        stmt = select(Artist)
        return self._db.scalars(stmt).all()

    def update_artist(self, entry: ArtistUpdate) -> Artist:
        logger.debug("Updating one artist entry...")

        with self._db.begin():
            artist_to_be_updated = entry.model_dump(exclude_unset=True)
            stmt = (
                update(Artist)
                .where(Artist.id == entry.id)
                .values(**artist_to_be_updated)
                .returning(Artist)
            )
            result = self._db.scalars(stmt).one()

        return result

    def delete_all(self) -> None:
        logger.debug("Deleting all entries from Artist table...")

        with self._db.begin():
            stmt = delete(Artist)
            num_deleted_rows = self._db.execute(stmt).rowcount  # pyright: ignore [reportAttributeAccessIssue]

            if not num_deleted_rows:
                error_msg = "Delete failed. Database is empty."
                logger.exception(error_msg)
                raise HTTPException(
                    detail=error_msg,
                    status_code=http_status.HTTP_404_NOT_FOUND,
                )

        logger.debug(f"Deleted {num_deleted_rows} row(s) from Artist table")

    def delete_artist(self, entry: ArtistDelete) -> None:
        with self._db.begin():
            stmt = delete(Artist).where(Artist.id == entry.id)
            num_deleted_rows = self._db.execute(stmt).rowcount  # pyright: ignore [reportAttributeAccessIssue]

            if not num_deleted_rows:
                error_msg = "Delete failed. Database is empty."
                logger.exception(error_msg)
                raise HTTPException(
                    detail=error_msg,
                    status_code=http_status.HTTP_404_NOT_FOUND,
                )

        logger.debug(f"Deleted entry {entry.id} from Artist table")
