from fastapi import Depends

from services.genre_service import  GenreService
from services.library_service import LibraryService
from services.catalog_service import CatalogService

from repositories.genre_repositories import GenreRepository
from repositories.library_repositories import LibraryRepository

from sqlalchemy.orm import Session
from database import get_session

def get_genre_repository(session: Session = Depends(get_session)) -> GenreRepository:
    return GenreRepository(session)

def get_library_repository(session: Session = Depends(get_session)) -> LibraryRepository:
    return LibraryRepository(session)

def get_genre_service(genre_repository: GenreRepository = Depends(get_genre_repository)
                      ) -> GenreService:
    return GenreService(genre_repository)

def get_library_service(genre_service: GenreService = Depends(get_genre_service),
                        library_repository: LibraryRepository = Depends(get_library_repository)
                        ) -> LibraryService:
    return LibraryService(genre_service, library_repository)

def get_catalog_service(genre_service: GenreService = Depends(get_genre_service), 
                        library_service: LibraryService = Depends(get_library_service)
                        ) -> CatalogService:
    return CatalogService(genre_service, library_service)
