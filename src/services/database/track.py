import logging
from collections.abc import Sequence

from sqlalchemy.orm import Session as OrmSession

from src.api.v1.artist.schema import ArtistCreate
from src.api.v1.genre.schema import GenreCreate
from src.api.v1.track.model import TrackModel as Track
from src.api.v1.track.schema import TrackCreate
from src.core.logging import Loggers
from src.services.operators.database import DatabaseOperator

logger = logging.getLogger(Loggers.DB)


class TrackService(DatabaseOperator):
    def __init__(self, session: OrmSession):
        self._db = session

    def create_track(
        self,
        entry: TrackCreate,
        artists: Sequence[ArtistCreate],
        genres: Sequence[GenreCreate],
    ) -> None:

        instance = Track(
            persistent_id=entry.persistent_id,
            name=entry.name,
            size=entry.size,
            total_time=entry.total_time,
        )

        instance.artists.extend(artists)
        instance.genres.extend(genres)

        with self._db.begin():
            self._db.add(instance)
