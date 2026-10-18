from typing import TYPE_CHECKING

from sqlalchemy import Integer, Interval, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.db.base import Base

if TYPE_CHECKING:
  from src.app.api.v1.artist.model import ArtistModel
  from src.app.api.v1.genre.model import GenreModel


class TrackModel(Base):
  __tablename__ = "track"

  persistent_id: Mapped[str] = mapped_column(String, primary_key=True)

  name: Mapped[str] = mapped_column(Text, nullable=False)

  size: Mapped[int] = mapped_column(Integer, nullable=False)

  total_time: Mapped[Interval] = mapped_column(Interval, nullable=False)

  year: Mapped[int] = mapped_column(Integer, nullable=False)

  bpm: Mapped[int] = mapped_column(Integer, nullable=True)

  bit_rate: Mapped[int] = mapped_column(Integer, nullable=False)

  sample_rate: Mapped[int] = mapped_column(Integer, nullable=False)

  file_type: Mapped[str] = mapped_column(String(6), nullable=True)

  artists: Mapped[list[ArtistModel]] = relationship(
    secondary="artist_track_assn_table",
    back_populates="tracks",
    passive_deletes=True,
    cascade="all, delete",
  )

  genres: Mapped[list[GenreModel]] = relationship(
    secondary="genre_track_assn_table",
    back_populates="tracks",
    passive_deletes=True,
    cascade="all, delete",
  )
