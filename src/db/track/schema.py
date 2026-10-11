"""
schema.py

Contains contracts for interacting with the Track database table
"""

from datetime import datetime
from pathlib import Path
from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    StringConstraints,
    ValidationError,
)


def _validate_file(file: Path) -> Path:
    file_path = Path(file)
    if not file_path.exists():
        raise ValidationError("File does not exist")
    return file_path


NonEmptyString = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1)
]
ValidString = NonEmptyString
OptionalValidString = ValidString | None
ValidFile = Annotated[Path, BeforeValidator(lambda v: _validate_file(v))]


class TrackBaseSchema(BaseModel):
    persistent_id: ValidString
    name: ValidString
    artist: ValidString


# ==============================
# CREATE
# ==============================


class TrackCreate(TrackBaseSchema):
    pass


# ==============================
# READ
# ==============================


class TrackRead(TrackBaseSchema):
    size: int
    total_time: int
    year: int
    bpm: int
    date_modified: datetime
    date_added: datetime
    bit_rate: int
    sample_rate: int
    file: ValidFile
    file_type: ValidString


# ==============================
# UPDATE
# ==============================


class TrackUpdate:
    pass


# ==============================
# DELETE
# ==============================


class TrackDelete:
    pass


# TODO: write the rest of these
