"""
schema.py

Contains contracts for interacting with the Track database table
"""

from datetime import timedelta
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any

from pydantic import (
    AfterValidator,
    BaseModel,
    Field,
)

from src.core.types import ValidInteger, ValidString


class AcceptableFileType(StrEnum):
    M4A = ".m4a"
    FLAC = ".flac"
    OGG = ".ogg"
    WAV = ".wav"


def _validate_file(file: Path) -> Path:
    if not file.exists():
        raise ValueError("File does not exist")
    return file


def _validate_file_type(file: Path) -> Path:
    if not file.suffix in AcceptableFileType.__members__:
        raise ValueError("Unacceptable file extension")
    return file


def _validate_interval(interval: Any) -> timedelta:
    if isinstance(interval, (int, float)):
        return timedelta(seconds=interval)

    elif isinstance(interval, timedelta):
        return interval

    else:
        raise TypeError("Unexpected interval type")


ValidFile = Annotated[Path, AfterValidator(_validate_file)]
ValidFileType = Annotated[ValidFile, AfterValidator(func=_validate_file_type)]
ValidInterval = Annotated[timedelta, AfterValidator(_validate_interval)]
ValidYear = Annotated[ValidInteger, Field(ge=1000, le=9999)]
ValidSampleRate = Annotated[ValidInteger, Field(ge=44100)]


class TrackBase(BaseModel):
    persistent_id: ValidString


class TrackCreate(TrackBase):
    name: ValidString
    artist: ValidString
    size: ValidInteger
    total_time: ValidInterval


class TrackRead(TrackBase):
    size: ValidInteger
    total_time: ValidInterval
    year: ValidYear
    bpm: ValidInteger
    bit_rate: ValidInteger
    sample_rate: ValidSampleRate
    file_type: ValidFileType


class TrackUpdate(TrackBase):
    pass


class TrackDelete(TrackBase):
    pass
