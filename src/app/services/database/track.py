import logging
from collections.abc import Sequence

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session as OrmSession

from src.app.api.v1.artist.model import ArtistModel as Artist
from src.app.api.v1.genre.model import GenreModel as Genre
from src.app.api.v1.track.model import TrackModel as Track
from src.app.api.v1.track.schema import (
  TrackBase,
  TrackCreate,
  TrackDelete,
  TrackUpdate,
)
from src.app.core.logging import Loggers
from src.app.services.operators.database import DatabaseOperator

logger = logging.getLogger(Loggers.DB)


class TrackService(DatabaseOperator):
  def __init__(self, session: OrmSession):
    self._db = session

  def create_track(
    self,
    entry: TrackCreate,
    artists: Sequence[Artist],
    genres: Sequence[Genre],
  ) -> Track:
    logger.debug("Creating Track entry...")

    track = Track(
      persistent_id=entry.persistent_id,
      name=entry.name,
      size=entry.size,
      total_time=entry.total_time,
      year=entry.year,
      bpm=entry.bpm,
      bit_rate=entry.bit_rate,
      sample_rate=entry.sample_rate,
      file_type=entry.file_type,
      album=entry.album,
    )

    with self._db.begin():
      for artist in artists:
        self._db.add(artist)
        artist.tracks.append(track)

      for genre in genres:
        self._db.add(genre)
        genre.tracks.append(track)

    return track

  def read_all(self) -> Sequence[Track]:
    logger.debug("Reading all track entries...")

    stmt = select(Track)
    return self._db.scalars(stmt).all()

  def read_track(self, entry: TrackBase) -> Track:
    logger.debug("Reading one track entry...")

    stmt = select(Track).where(Track.persistent_id == entry.persistent_id)
    return self._db.scalars(stmt).one()

  def update_track(self, entry: TrackUpdate) -> Track:
    logger.debug("Updating one track entry...")

    with self._db.begin():
      track_to_be_updated = entry.model_dump(exclude_unset=True)
      stmt = (
        update(Track)
        .where(Track.persistent_id == entry.persistent_id)
        .values(**track_to_be_updated)
        .returning(Track)
      )
      result = self._db.scalars(stmt).one()

    return result

  def delete_all(self) -> None:
    logger.debug("Deleting all entries from Track table...")

    with self._db.begin():
      stmt = delete(Track)
      num_deleted_rows = self._db.execute(stmt).rowcount  # pyright: ignore [reportAttributeAccessIssue]

      if not num_deleted_rows:
        error_msg = "Delete failed. Database is empty."
        logger.exception(error_msg)
        raise HTTPException(
          detail=error_msg,
          status_code=http_status.HTTP_404_NOT_FOUND,
        )

    logger.debug(f"Deleted {num_deleted_rows} row(s) from Track table")

  def delete_track(self, entry: TrackDelete) -> None:
    with self._db.begin():
      stmt = delete(Track).where(Track.persistent_id == entry.persistent_id)
      num_deleted_rows = self._db.execute(stmt).rowcount  # pyright: ignore [reportAttributeAccessIssue]

      if not num_deleted_rows:
        error_msg = "Delete failed. Database is empty."
        logger.exception(error_msg)
        raise HTTPException(
          detail=error_msg,
          status_code=http_status.HTTP_404_NOT_FOUND,
        )

    logger.debug(f"Deleted entry {entry.persistent_id} from Track table")
