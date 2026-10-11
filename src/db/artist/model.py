from collections.abc import Set

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.associations import artist_track_assn_table
from db.base import Base
from db.track.model import TrackModel as Track


class ArtistModel(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    tracks: Mapped[Set["Track"]] = relationship(
        secondary=artist_track_assn_table,
        back_populates="persistent_id",
        cascade="all, delete-orphan",
    )
