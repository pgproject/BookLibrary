from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import Base

if TYPE_CHECKING:
    from models.book import Book

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list["Book"]] = relationship(back_populates="genre")