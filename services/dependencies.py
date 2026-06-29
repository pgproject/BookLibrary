from services.genre_service import GenreService
from services.library_service import LibraryService
from services.catalog_service import CatalogService

genre_service = GenreService()
library_service = LibraryService(genre_service)
catalog_service = CatalogService(genre_service, library_service)

