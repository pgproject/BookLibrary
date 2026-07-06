from fastapi import Depends

from services.genre_service import  GenreService
from services.library_service import LibraryService
from services.catalog_service import CatalogService

from database import get_session

session = get_session()

def get_genre_service(session = Depends(get_session)):
    return GenreService(session)

def get_library_service(session = Depends(get_session), genre_service = Depends(get_genre_service)):
    return LibraryService(session, genre_service)

def get_catalog_service(genre_service = Depends(get_genre_service), library_service = Depends(get_library_service)):
    return CatalogService(genre_service, library_service)