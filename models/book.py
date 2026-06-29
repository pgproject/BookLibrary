from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import Base

if TYPE_CHECKING:
    from models.genre import Genre

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id")) 
    genre: Mapped["Genre"] = relationship(back_populates = "books") 