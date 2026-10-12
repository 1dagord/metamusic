"""
schema.py

Contains contracts for interacting with the Artist database table
"""

from pydantic import BaseModel, NonNegativeInt

from src.api.v1.track.schema import TrackRead
from src.core.types import ValidString


class ArtistBase(BaseModel):
    id: NonNegativeInt


class ArtistCreate(BaseModel):
    name: ValidString


class ArtistRead(ArtistBase):
    name: ValidString
    tracks: set[TrackRead]


class ArtistUpdate(ArtistBase):
    name: ValidString
    tracks: set[TrackRead]


class ArtistDelete(ArtistBase):
    pass
