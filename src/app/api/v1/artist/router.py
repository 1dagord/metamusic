from re import M

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.app.api.v1.artist.schema import ArtistBase, ArtistCreate, ArtistRead
from src.app.core.types import DatabaseSession
from src.app.services.database.artist import ArtistService

ArtistRouter = APIRouter(tags=["Artist"], prefix="/artist")


def get_artist_service(db: DatabaseSession) -> ArtistService:
    return ArtistService(session=db)


# ==============================
# CREATE
# ==============================


@ArtistRouter.post(
    "/create",
    summary="Create an Artist table entry",
    response_model=ArtistRead,
    status_code=http_status.HTTP_201_CREATED,
)
def create_artist(
    entry: ArtistCreate,
    artist_service: ArtistService = Depends(get_artist_service),
):
    return artist_service.create_artist(entry)


# ==============================
# READ
# ==============================


@ArtistRouter.get(
    "/read",
    summary="Read an Artist table entry",
    response_model=list[ArtistRead],
    status_code=http_status.HTTP_200_OK,
)
def read_artist(
    entries: list[ArtistBase],
    artist_service: ArtistService = Depends(get_artist_service),
):
    return artist_service.read_artist(entries)


@ArtistRouter.get(
    "/read/all",
    summary="Read *all* Artist table entries",
    response_model=list[ArtistRead],
    status_code=http_status.HTTP_200_OK,
)
def read_all(
    artist_service: ArtistService = Depends(get_artist_service),
):
    return artist_service.read_all()


# ==============================
# UPDATE
# ==============================


# ==============================
# DELETE
# ==============================


@ArtistRouter.delete(
    "/delete/all",
    summary="Delete *all* entries to Artist table",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_all(artist_service: ArtistService = Depends(get_artist_service)):
    return artist_service.delete_all()
