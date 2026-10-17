from collections.abc import Sequence

from pydantic import BaseModel, NonNegativeInt

from src.app.api.v1.track.schema import TrackRead
from src.app.core.types import OptionalValidString, ValidString


class GenreBase(BaseModel):
    id: NonNegativeInt


class GenreCreate(BaseModel):
    name: ValidString


class GenreRead(GenreBase):
    name: ValidString
    tracks: Sequence[TrackRead]


class GenreUpdate(GenreBase):
    name: OptionalValidString = None
    tracks: Sequence[TrackRead] | None = None


class GenreDelete(GenreBase):
    pass
