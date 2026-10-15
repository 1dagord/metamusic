from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.app.db.base import Base


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
