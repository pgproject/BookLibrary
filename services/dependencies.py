from fastapi import Depends

from services.genre_service import  GenreService
from services.library_service import LibraryService
from services.catalog_service import CatalogService

from sqlalchemy.orm import Session
from database import get_session

def get_genre_service(session: Session = Depends(get_session)) -> GenreService:
    return GenreService(session)

def get_library_service(session: Session = Depends(get_session), 
                        genre_service: GenreService = Depends(get_genre_service)) -> LibraryService:
    return LibraryService(session, genre_service)

def get_catalog_service(genre_service: 
                        GenreService = Depends(get_genre_service), 
                        library_service: LibraryService = Depends(get_library_service)) -> CatalogService:
    return CatalogService(genre_service, library_service)