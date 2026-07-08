from fastapi import APIRouter, Depends, status

from models.genre import Genre  

from schemas.genre import GenreCreate, GenreResponses

from services.catalog_service import CatalogService
from services.dependencies import get_catalog_service, get_genre_service
from services.genre_service import GenreService

router = APIRouter (
    prefix = "/genre",
    tags = ["genre"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_genre(genre: GenreCreate, genre_service: GenreService = Depends(get_genre_service)):
    new_genre = Genre(name= genre.name)
    
    genre_service.add_genre(new_genre)
    return {"message": "Genre added successfully!"}

@router.delete("/{name}")
def remove_genre(name: str, catalog_service: CatalogService = Depends(get_catalog_service)):
    catalog_service.remove_genre(name)
    return {"message": "Genre removed successfully!"}
    
@router.get("/", response_model=list[GenreResponses])
def get_genres(genre_service: GenreService = Depends(get_genre_service)):
    return genre_service.get_genres()