import logging
from collections.abc import Generator
from typing import Annotated, Any

from fastapi import APIRouter, Depends, UploadFile
from fastapi import status as http_status
from pydantic import ValidationError
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.orm import sessionmaker

from src.app.api.v1.artist.model import ArtistModel as Artist
from src.app.api.v1.artist.schema import ArtistCreate
from src.app.api.v1.genre.model import GenreModel as Genre
from src.app.api.v1.genre.router import GenreService
from src.app.api.v1.genre.schema import GenreCreate
from src.app.api.v1.track.schema import (
    TrackBase,
    TrackCreate,
    TrackDelete,
    TrackRead,
    TrackUpdate,
)
from src.app.core.config import config
from src.app.core.logging import Loggers
from src.app.core.types import DatabaseSession
from src.app.db.config import engine
from src.app.services.database.artist import ArtistService
from src.app.services.database.track import TrackService
from src.app.services.io.parser import IOService
from src.app.services.operators.file import FileOperator

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


def get_io_service() -> IOService:
    return IOService()


# ==============================
# CREATE
# ==============================


@TrackRouter.post(
    "/create",
    summary="Create a Track table entry containing one or more Genre and Artist",
    response_model=TrackRead,
    status_code=http_status.HTTP_201_CREATED,
)
def create_track(
    entry: TrackCreate,
    track_service: Annotated[TrackService, Depends(get_track_service)],
    artist_service: Annotated[ArtistService, Depends(get_artist_service)],
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    artists = artist_service.create_artist_from_track(entry)
    genres = genre_service.create_genre_from_track(entry)
    return track_service.create_track(entry, artists, genres)


@TrackRouter.post(
    "/create/upload",
    summary="Create a Track table entry from an uploaded file",
    response_model=list[TrackRead],
    status_code=http_status.HTTP_201_CREATED,
)
def create_tracks_from_file(
    file: UploadFile,
    io_service: Annotated[IOService, Depends(get_io_service)],
    track_service: Annotated[TrackService, Depends(get_track_service)],
    artist_service: Annotated[ArtistService, Depends(get_artist_service)],
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    content = file.file.read()
    track_data = io_service.parse(content).get("Tracks").values()

    created_tracks = []

    for obj in track_data:
        # skip track if validation fails (not enough metadata)
        try:
            entry = TrackCreate.model_validate(obj)
        except ValidationError:
            continue

        artists = artist_service.create_artist_from_track(entry)
        genres = genre_service.create_genre_from_track(entry)

        logger.debug("Creating Track from file data...")

        created_tracks.append(
            track_service.create_track(entry, artists, genres)
        )

    logger.debug(f"Created {len(created_tracks)} of {len(track_data)} tracks")

    return created_tracks


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
    track_service: Annotated[TrackService, Depends(get_track_service)],
):
    return track_service.read_all()


@TrackRouter.get(
    "/read",
    summary="Read a Track table entry",
    response_model=TrackRead,
    status_code=http_status.HTTP_200_OK,
)
def read_track(
    entry: TrackBase,
    track_service: Annotated[TrackService, Depends(get_track_service)],
):
    return track_service.read_track(entry)


# ==============================
# UPDATE
# ==============================


@TrackRouter.patch(
    "/update",
    summary="Update a Track table entry",
    response_model=TrackRead,
    status_code=http_status.HTTP_200_OK,
)
def update_track(
    entry: TrackUpdate,
    track_service: Annotated[TrackService, Depends(get_track_service)],
):
    return track_service.update_track(entry)


# ==============================
# DELETE
# ==============================


@TrackRouter.delete(
    "/delete/all",
    summary="Delete *all* entries from Track table",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_all(
    track_service: Annotated[TrackService, Depends(get_track_service)],
):
    return track_service.delete_all()


@TrackRouter.delete(
    "/delete",
    summary="Delete one entry from Track table",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_track(
    entry: TrackDelete,
    track_service: Annotated[TrackService, Depends(get_track_service)],
):
    return track_service.delete_track(entry)
