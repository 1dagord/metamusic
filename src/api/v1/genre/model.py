from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.associations import GenreTrackAssociation


class GenreModel(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    tracks: Mapped[list["GenreTrackAssociation"]] = relationship(
        back_populates="genre",
        cascade="all, delete-orphan",
    )
