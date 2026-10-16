from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.db.base import Base

if TYPE_CHECKING:
    from src.app.api.v1.track.model import TrackModel
    # from src.app.db.associations import GenreTrackAssociation


class GenreModel(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    tracks: Mapped[list["TrackModel"]] = relationship(
        secondary="genre_track_assn_table",
        back_populates="genres",
        passive_deletes=True,
        passive_updates=True,
    )
