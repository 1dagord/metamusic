"""
schema.py

Contains contracts for interacting with the Track database table
"""

import re
from datetime import timedelta
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import unquote, urlparse
from urllib.request import url2pathname

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    Field,
    StringConstraints,
)

from src.app.core.types import (
    OptionalValidInteger,
    OptionalValidString,
    ValidInteger,
    ValidString,
)


class AcceptableFileType(StrEnum):
    M4A = ".m4a"
    M4P = ".m4p"
    FLAC = ".flac"
    OGG = ".ogg"
    WAV = ".wav"


def _validate_file(file_name: str) -> str:
    parsed_url = urlparse(file_name)
    parsed_file_name = unquote(url2pathname(parsed_url.path))

    normalized_file_name = Path(unquote(parsed_file_name))
    if not normalized_file_name.exists():
        raise ValueError("File does not exist")
    return normalized_file_name.suffix


def _validate_file_type(file_type: str) -> str:
    if not file_type in [member.value for member in AcceptableFileType]:
        raise ValueError("Unacceptable file extension")
    return file_type


def _validate_interval(interval: Any) -> timedelta:
    if isinstance(interval, int):
        return timedelta(milliseconds=interval)

    elif isinstance(interval, timedelta):
        return interval

    else:
        raise TypeError("Unexpected interval type")


def _validate_artists(string: str) -> set[str]:
    artists = set(re.split(r"[,&]", string))
    return artists


def _validate_genres(string: str) -> set[str]:
    genres = set(re.split(r"[,&]", string))
    return genres


ValidFile = Annotated[str, BeforeValidator(_validate_file)]
ValidFileType = Annotated[
    str,
    AfterValidator(func=_validate_file_type),
    StringConstraints(min_length=1, max_length=6),
]
ValidInterval = Annotated[timedelta, AfterValidator(_validate_interval)]
ValidYear = Annotated[ValidInteger, Field(ge=1000, le=9999)]
ValidSampleRate = Annotated[ValidInteger, Field(ge=44100)]
ValidArtists = Annotated[set[ValidString], BeforeValidator(_validate_artists)]
ValidGenres = Annotated[set[ValidString], BeforeValidator(_validate_genres)]

OptionalValidYear = ValidYear | None
OptionalValidInterval = ValidInterval | None
OptionalValidSampleRate = ValidSampleRate | None
OptionalValidFile = ValidFile | None
OptionalValidFileType = ValidFileType | None


class TrackBase(BaseModel):
    persistent_id: ValidString


class TrackCreate(BaseModel):
    persistent_id: ValidString = Field(alias="Persistent ID")
    name: ValidString = Field(alias="Name")
    size: ValidInteger = Field(alias="Size")
    total_time: ValidInterval = Field(alias=("Total Time"))
    year: ValidYear = Field(alias=("Year"))
    bpm: OptionalValidInteger = Field(alias=("BPM"), default=None)
    bit_rate: OptionalValidInteger = Field(alias=("Bit Rate"), default=None)
    sample_rate: ValidSampleRate = Field(alias=("Sample Rate"))
    file_type: OptionalValidFile = Field(alias=("Location"), default=None)
    artists: ValidArtists = Field(alias="Artist")
    genres: ValidGenres = Field(default_factory=set)


class TrackRead(TrackBase):
    name: ValidString
    size: ValidInteger
    total_time: ValidInterval
    year: ValidYear
    bpm: OptionalValidInteger = None
    bit_rate: ValidInteger
    sample_rate: ValidSampleRate
    file_type: OptionalValidFileType = None


class TrackUpdate(TrackBase):
    name: OptionalValidString = None
    size: OptionalValidInteger = None
    total_time: OptionalValidInterval = None
    year: OptionalValidYear = None
    bpm: OptionalValidInteger = None
    bit_rate: OptionalValidInteger = None
    sample_rate: OptionalValidSampleRate = None
    file_type: OptionalValidFileType = None


class TrackDelete(BaseModel):
    persistent_id: ValidString = Field(alias="Persistent ID")
