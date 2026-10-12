from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.associations import ArtistTrackAssociation


class ArtistModel(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    tracks: Mapped[list["ArtistTrackAssociation"]] = relationship(
        back_populates="artist",
        cascade="all, delete-orphan",
    )
