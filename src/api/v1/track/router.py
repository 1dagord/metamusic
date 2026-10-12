from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.api.v1.genre.router import GenreService
from src.api.v1.track.schema import TrackCreate
from src.core.types import DatabaseSession
from src.services.database.artist import ArtistService
from src.services.database.track import TrackService

TrackRouter = APIRouter(tags=["Track"], prefix="/track")


def get_track_service(db: DatabaseSession) -> TrackService:
    return TrackService(session=db)


def get_artist_service(db: DatabaseSession) -> ArtistService:
    return ArtistService(session=db)


def get_genre_service(db: DatabaseSession) -> GenreService:
    return GenreService(session=db)


# ==============================
# CREATE
# ==============================

# TODO: figure out semantics of one track with multiple artists


@TrackRouter.post(
    "/create",
    summary="Create a Track table entry containing one or more Genre and Artist",
    status_code=http_status.HTTP_201_CREATED,
)
def create_track(
    entry: TrackCreate,
    track_service: TrackService = Depends(get_track_service),
    artist_service: ArtistService = Depends(get_artist_service),
    genre_service: GenreService = Depends(get_genre_service),
) -> None:
    artists = artist_service.create_artist()
    genres = genre_service.create_genre()
    return track_service.create_track(entry, artists, genres)


# ==============================
# READ
# ==============================


# ==============================
# UPDATE
# ==============================


# ==============================
# DELETE
# ==============================
