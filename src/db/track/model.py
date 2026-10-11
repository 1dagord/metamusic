from collections.abc import Set

from sqlalchemy import Integer, Interval, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.associations import artist_track_assn_table, genre_track_assn_table
from db.base import Base
from src.db.artist.model import ArtistModel as Artist
from src.db.genre.model import GenreModel as Genre


class TrackModel(Base):
    __tablename__ = "track"

    persistent_id: Mapped[int] = mapped_column(String, primary_key=True)

    name: Mapped[str] = mapped_column(Text, nullable=False)

    size: Mapped[int] = mapped_column(Integer, nullable=False)

    total_time: Mapped[Interval] = mapped_column(Interval, nullable=False)

    artists: Mapped[Set["Artist"]] = relationship(
        secondary=artist_track_assn_table,
        back_populates="id",
        cascade="all, delete-orphan",
    )

    genres: Mapped[Set["Genre"]] = relationship(
        secondary=genre_track_assn_table,
        back_populates="id",
        cascade="all, delete-orphan",
    )
