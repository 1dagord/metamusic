import logging
from collections.abc import Sequence

from sqlalchemy.orm import Session as OrmSession

from src.api.v1.artist.model import ArtistModel as Artist
from src.api.v1.artist.schema import ArtistCreate
from src.core.logging import Loggers
from src.services.operators.database import DatabaseOperator

logger = logging.getLogger(Loggers.DB)


class ArtistService(DatabaseOperator):
    def __init__(self, session: OrmSession):
        self._db = session

    def create_artist(self, entries: Sequence[ArtistCreate]) -> None:
        with self._db.begin():
            self._db.add_all(
                [
                    Artist(
                        name=entry.name,
                    )
                    for entry in entries
                ]
            )
