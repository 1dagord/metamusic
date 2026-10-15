"""
schema.py

Contains contracts for interacting with the Artist database table
"""

from collections.abc import Sequence

from pydantic import BaseModel, NonNegativeInt

from src.app.api.v1.track.schema import TrackRead
from src.app.core.types import ValidString


class ArtistBase(BaseModel):
    id: NonNegativeInt


class ArtistCreate(BaseModel):
    name: ValidString


class ArtistRead(ArtistBase):
    name: ValidString
    tracks: Sequence[TrackRead]


class ArtistUpdate(ArtistBase):
    name: ValidString
    tracks: Sequence[TrackRead]


class ArtistDelete(ArtistBase):
    pass
