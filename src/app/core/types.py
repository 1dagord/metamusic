from datetime import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import NonNegativeInt, StringConstraints
from sqlalchemy.orm import Session as OrmSession

from src.app.db.config import get_db_session

DatabaseSession = Annotated[OrmSession, Depends(get_db_session)]


# Validation Types

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
ValidString = NonEmptyString
ValidInteger = NonNegativeInt
ValidDateTime = datetime

OptionalValidString = ValidString | None
OptionalValidInteger = ValidInteger | None
