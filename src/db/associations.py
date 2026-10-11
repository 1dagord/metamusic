from sqlalchemy import Column, ForeignKey, Table

from db.base import Base

artist_track_assn_table = Table(
    "artist_track_assn_table",
    Base.metadata,
    Column(
        "artist_id",
        ForeignKey("artist.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "track_id",
        ForeignKey("track.persistent_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

genre_track_assn_table = Table(
    "genre_track_assn_table",
    Base.metadata,
    Column(
        "genre_id", ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "track_id",
        ForeignKey("track.persistent_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
