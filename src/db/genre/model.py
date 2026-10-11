from collections.abc import Set

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from src.db.associations import genre_track_assn_table
from src.db.track.model import TrackModel as Track


class GenreModel(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    tracks: Mapped[Set["Track"]] = relationship(
        secondary=genre_track_assn_table,
        back_populates="persistent_id",
        cascade="all, delete-orphan",
    )
