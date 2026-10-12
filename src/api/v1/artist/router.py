from fastapi import APIRouter

from src.core.types import DatabaseSession
from src.services.database.artist import ArtistService

ArtistRouter = APIRouter(tags=["Artist"], prefix="/artist")


def get_artist_service(db: DatabaseSession) -> ArtistService:
    return ArtistService(session=db)


# ==============================
# CREATE
# ==============================

# ==============================
# READ
# ==============================


# ==============================
# UPDATE
# ==============================


# ==============================
# DELETE
# ==============================
