from sqlalchemy.orm import Session
from sqlalchemy import select


from models.genre import Genre

class GenreRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_genre(self, new_genre: Genre):
        self.session.add(new_genre)
        self.session.commit()

    def remove_genre(self, genre: Genre):
        self.session.delete(genre)
        self.session.commit()
    
    def find_genre_by_name(self, name: str)-> Genre | None:
        return self.session.scalar(
            select(Genre)
            .where(Genre.name == name)
        )
    
    def find_all_genres(self) -> list[Genre]:
        return self.session.scalars(
            select(Genre)
            .order_by(Genre.name)
        ).all()
