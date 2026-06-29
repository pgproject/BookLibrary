from sqlalchemy import select

from database import SessionLocal

from models.genre import Genre

class GenreService:
    def __init__(self):
        self.session = SessionLocal()

    def add_genre(self, newGenre) -> bool:

        genre = self.session.scalar(
            select(Genre)
            .where(Genre.name == newGenre.name)
        )

        if genre:
            return False

        self.session.add(newGenre)
        self.session.commit()
        return True

    def remove_genre(self, name: str) -> bool:
        genre = self.session.scalar(
            select(Genre)
            .where(Genre.name == name)
        )
        if genre:
            self.session.delete(genre)
            self.session.commit()
            return True
        return False

    def genre_exists(self, name: str) -> bool:
        genre = self.session.scalar(
            select(Genre)
            .where(Genre.name == name)
        )

        if genre:
            return True
        return False

    def get_genres(self):
        return self.session.scalars(
            select(Genre)
            .order_by(Genre.name)
        ).all()
    
    def get_genre_id(self, name: str):
        genre = self.session.scalar(
            select(Genre)
            .where(Genre.name == name)
        )
        return genre.id
    