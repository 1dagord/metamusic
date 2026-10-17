from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.db.base import Base

if TYPE_CHECKING:
    from src.app.api.v1.track.model import TrackModel


class ArtistModel(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    tracks: Mapped[list[TrackModel]] = relationship(
        secondary="artist_track_assn_table",
        back_populates="artists",
        passive_deletes=True,
        passive_updates=True,
    )
