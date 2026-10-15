import logging
from collections.abc import Sequence

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session as OrmSession

from src.app.api.v1.artist.model import ArtistModel as Artist
from src.app.api.v1.artist.schema import ArtistBase, ArtistCreate, ArtistRead
from src.app.api.v1.track.schema import TrackCreate
from src.app.core.logging import Loggers
from src.app.services.operators.database import DatabaseOperator

logger = logging.getLogger(Loggers.DB)


class ArtistService(DatabaseOperator):
    def __init__(self, session: OrmSession):
        self._db = session

    def create_artist(self, entry: ArtistCreate):
        logger.debug("Creating Artist entry...")

        with self._db.begin():
            stmt = insert(Artist).values(name=entry.name).returning(Artist)
            result = self._db.scalars(stmt).one()  # pyright: ignore [reportCallIssue, reportArgumentType]

        logger.debug("Created Artist entry")
        return result

    # TODO: write this
    def create_artist_from_track(self, track: TrackCreate) -> Sequence[Artist]:
        logger.debug("Creating Artist from Track entry...")

        instances = []

        with self._db.begin():
            select_stmt = select(Artist).where(Artist.name.in_(track.artists))
            results = self._db.scalars(select_stmt).all()
            present_artists = results
            # stores current ArtistModel objects...
            instances.extend(present_artists)

        # ...and creates new ones for those not present
        instances.extend(
            [
                Artist(name=artist)
                for artist in track.artists
                if artist not in present_artists
            ]
        )

        with self._db.begin():
            self._db.add_all(instances)

        return instances

    def read_artist(self, entry: ArtistBase):
        stmt = select(Artist).where(Artist.id == entry.id)
        return self._db.scalars(stmt).one()

    def read_all(self) -> Sequence[Artist]:
        logger.debug("Reading all artist entries...")

        stmt = select(Artist)
        return self._db.scalars(stmt).all()

    def delete_all(self):
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

        logger.debug(f"Deleted {num_deleted_rows} from Artist table")
