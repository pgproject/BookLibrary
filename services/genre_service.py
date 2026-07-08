from models.genre import Genre
from repositories.genre_repositories import GenreRepository

from exceptions.genre_exceptions import GenreAlreadyExistsException, GenreNotFoundException

class GenreService:
    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    def add_genre(self, new_genre: Genre):
        genre = self.genre_repository.find_genre_by_name(new_genre.name)

        if genre:
            raise GenreAlreadyExistsException()

        self.genre_repository.add_genre(new_genre)

    def remove_genre(self, name: str):
        genre = self.genre_repository.find_genre_by_name(name)

        if not genre:
            raise GenreNotFoundException()

        self.genre_repository.remove_genre(genre)

    def get_genres(self)-> list[Genre]:
        return self.genre_repository.find_all_genres()

    def get_genre_id(self, name: str)-> int:
        genre = self.genre_repository.find_genre_by_name(name)

        if not genre:
            raise GenreNotFoundException()

        return genre.id
    