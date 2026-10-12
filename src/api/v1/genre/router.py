from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.api.v1.genre.schema import GenreBase, GenreCreate, GenreRead
from src.core.types import DatabaseSession
from src.services.database.genre import GenreService

GenreRouter = APIRouter(tags=["Genre"], prefix="/genre")


def get_genre_service(db: DatabaseSession) -> GenreService:
    return GenreService(session=db)


# ==============================
# CREATE
# ==============================


@GenreRouter.post(
    "/create",
    summary="Create a Genre table entry",
    status_code=http_status.HTTP_201_CREATED,
)
def create_entry(
    entries: list[GenreCreate],
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.create_genre(entries)


# ==============================
# READ
# ==============================


@GenreRouter.get(
    "/read/all",
    summary="Read *all* Genre table entries",
    response_model=list[GenreRead],
    status_code=http_status.HTTP_200_OK,
)
def read_all(
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.read_all()


@GenreRouter.get(
    "/read",
    summary="Read a Genre table entry",
    response_model=list[GenreRead],
    status_code=http_status.HTTP_200_OK,
)
def read_entry(
    entries: list[GenreBase],
    genre_service: GenreService = Depends(get_genre_service),
):
    return genre_service.read_genre(entries)


# ==============================
# UPDATE
# ==============================


# ==============================
# DELETE
# ==============================
