from typing import TYPE_CHECKING

from sqlalchemy import Integer, Interval, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.associations import (
        ArtistTrackAssociation,
        GenreTrackAssociation,
    )


class TrackModel(Base):
    __tablename__ = "track"

    persistent_id: Mapped[int] = mapped_column(String, primary_key=True)

    name: Mapped[str] = mapped_column(Text, nullable=False)

    size: Mapped[int] = mapped_column(Integer, nullable=False)

    total_time: Mapped[Interval] = mapped_column(Interval, nullable=False)

    artists: Mapped[list["ArtistTrackAssociation"]] = relationship(
        back_populates="track",
        cascade="all, delete-orphan",
    )

    genres: Mapped[list["GenreTrackAssociation"]] = relationship(
        back_populates="track",
        cascade="all, delete-orphan",
    )
