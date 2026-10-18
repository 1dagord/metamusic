from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.app.api.v1.genre.schema import (
  GenreBase,
  GenreCreate,
  GenreDelete,
  GenreRead,
  GenreUpdate,
)
from src.app.core.types import DatabaseSession
from src.app.services.database.genre import GenreService

GenreRouter = APIRouter(tags=["Genre"], prefix="/genre")


def get_genre_service(db: DatabaseSession) -> GenreService:
  return GenreService(session=db)


# ==============================
# CREATE
# ==============================


@GenreRouter.post(
  "/create",
  summary="Create a Genre table entry",
  response_model=GenreRead,
  status_code=http_status.HTTP_201_CREATED,
)
def create_genre(
  entry: GenreCreate,
  genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
  return genre_service.create_genre(entry)


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
  genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
  return genre_service.read_all()


@GenreRouter.get(
  "/read",
  summary="Read a Genre table entry",
  response_model=list[GenreRead],
  status_code=http_status.HTTP_200_OK,
)
def read_genre(
  entry: GenreBase,
  genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
  return genre_service.read_genre(entry)


# ==============================
# UPDATE
# ==============================


@GenreRouter.patch(
  "/update",
  summary="Update a Genre table entry",
  response_model=GenreRead,
  status_code=http_status.HTTP_200_OK,
)
def update_genre(
  entry: GenreUpdate,
  genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
  return genre_service.update_genre(entry)


# ==============================
# DELETE
# ==============================


@GenreRouter.delete(
  "/delete/all",
  summary="Delete *all* entries to Genre table",
  status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_all(
  genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
  return genre_service.delete_all()


@GenreRouter.delete(
  "/delete",
  summary="Delete one entry to Genre table",
  status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_genre(
  entry: GenreDelete,
  genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
  return genre_service.delete_genre(entry)
