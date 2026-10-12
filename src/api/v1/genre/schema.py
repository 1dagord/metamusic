"""
schema.py

Contains contracts for interacting with the Genre database table
"""

from pydantic import BaseModel, NonNegativeInt

from src.api.v1.track.schema import TrackRead
from src.core.types import ValidString


class GenreBase(BaseModel):
    id: NonNegativeInt


class GenreCreate(BaseModel):
    name: ValidString


class GenreRead(GenreBase):
    name: ValidString
    tracks: set[TrackRead]


class GenreUpdate(GenreBase):
    pass


class GenreDelete(GenreBase):
    pass
