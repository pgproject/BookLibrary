from sqlalchemy import select

from sqlalchemy.orm import Session

from models.genre import Genre
from exceptions.genre_exceptions import GenreAlreadyExistsException, GenreNotFoundException

class GenreService:
    def __init__(self, session: Session):
        self.session = session

    def add_genre(self, new_genre: Genre):

        genre = self.session.scalar(
            select(Genre)
            .where(Genre.name == new_genre.name)
        )

        if genre:
            raise GenreAlreadyExistsException()

        self.session.add(new_genre)
        self.session.commit()

    def remove_genre(self, name: str):
        genre = self.session.scalar(
            select(Genre)
            .where(Genre.name == name)
        )
        if not genre:
            raise GenreNotFoundException()

        self.session.delete(genre)
        self.session.commit()

    def get_genres(self)-> list[Genre]:
        return self.session.scalars(
            select(Genre)
            .order_by(Genre.name)
        ).all()
    
    def get_genre_id(self, name: str):
        genre = self.session.scalar(
            select(Genre)
            .where(Genre.name == name)
        )
        if not genre:
            raise GenreNotFoundException()

        return genre.id
    