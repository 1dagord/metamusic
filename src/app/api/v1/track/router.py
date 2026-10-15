import logging
from collections.abc import Generator
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status as http_status
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.orm import sessionmaker

from src.app.api.v1.artist.model import ArtistModel as Artist
from src.app.api.v1.artist.schema import ArtistCreate
from src.app.api.v1.genre.model import GenreModel as Genre
from src.app.api.v1.genre.router import GenreService
from src.app.api.v1.genre.schema import GenreCreate
from src.app.api.v1.track.schema import TrackCreate, TrackRead
from src.app.core.logging import Loggers
from src.app.core.types import DatabaseSession
from src.app.db.config import engine
from src.app.services.database.artist import ArtistService
from src.app.services.database.track import TrackService

TrackRouter = APIRouter(tags=["Track"], prefix="/track")

logger = logging.getLogger(Loggers.DB)


def _get_second_db_session() -> Generator[OrmSession]:
    logger.debug("=== Getting second database session... ===")
    SecondSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    second_db = SecondSessionLocal()
    try:
        yield second_db
    finally:
        second_db.close()


def _get_third_db_session() -> Generator[OrmSession]:
    logger.debug("=== Getting third database session... ===")
    ThirdSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    third_db = ThirdSessionLocal()
    try:
        yield third_db
    finally:
        third_db.close()


SecondDatabaseSession = Annotated[OrmSession, Depends(_get_second_db_session)]
ThirdDatabaseSession = Annotated[OrmSession, Depends(_get_third_db_session)]


def get_track_service(db: DatabaseSession) -> TrackService:
    return TrackService(session=db)


def get_artist_service(db: SecondDatabaseSession) -> ArtistService:
    return ArtistService(session=db)


def get_genre_service(db: ThirdDatabaseSession) -> GenreService:
    return GenreService(session=db)


# ==============================
# CREATE
# ==============================

# TODO: figure out semantics of one track with multiple artists


@TrackRouter.post(
    "/create",
    summary="Create a Track table entry containing one or more Genre and Artist",
    response_model=TrackRead,
    status_code=http_status.HTTP_201_CREATED,
)
def create_track(
    entry: TrackCreate,
    track_service: TrackService = Depends(get_track_service),
    artist_service: ArtistService = Depends(get_artist_service),
    genre_service: GenreService = Depends(get_genre_service),
):
    # TODO: entering same track results in a HTTP 201; figure out a way to force a collision
    # (this didn't work; don't make it hacky)

    artists = artist_service.create_artist_from_track(entry)

    logger.debug(f"{[a.name for a in artists] = }")

    genres = genre_service.create_genre_from_track(entry)

    logger.debug(f"{[g.name for g in genres] = }")

    return track_service.create_track(entry, artists, genres)


# ==============================
# READ
# ==============================


@TrackRouter.get(
    "/read/all",
    summary="Read *all* Track table entries",
    response_model=list[TrackRead],
    status_code=http_status.HTTP_200_OK,
)
def read_all(
    track_service: TrackService = Depends(get_track_service),
):
    return track_service.read_all()


# ==============================
# UPDATE
# ==============================


# ==============================
# DELETE
# ==============================


@TrackRouter.delete(
    "/delete/all",
    summary="Delete *all* entries to Track table",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_all(track_service: TrackService = Depends(get_track_service)):
    return track_service.delete_all()
