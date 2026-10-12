from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.v1.artist.model import ArtistModel as Artist
from src.api.v1.genre.model import GenreModel as Genre
from src.api.v1.track.model import TrackModel as Track
from src.db.base import Base


class ArtistTrackAssociation(Base):
    __tablename__ = "artist_track_assn_table"

    artist_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="artist.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    track_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="track.persistent_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    artist: Mapped["Artist"] = relationship(back_populates="tracks")
    track: Mapped["Track"] = relationship(back_populates="artists")


class GenreTrackAssociation(Base):
    __tablename__ = "genre_track_assn_table"

    genre_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="genre.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    track_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="track.persistent_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    genre: Mapped["Genre"] = relationship(back_populates="tracks")
    track: Mapped["Track"] = relationship(back_populates="genres")
