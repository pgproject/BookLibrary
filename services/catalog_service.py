from exceptions.genre_exceptions import GenreIsUsedException, GenreNotFoundException
from services.genre_service import GenreService
from services.library_service import LibraryService

class CatalogService:

    def __init__(
            self,
            genre_service: GenreService,
            library_service: LibraryService
        ):
            self.genre_service = genre_service
            self.library_service = library_service

    def remove_genre(self, name: str):
        
        if self.library_service.genre_is_used(name):
            raise GenreIsUsedException()
        
        self.genre_service.remove_genre(name)