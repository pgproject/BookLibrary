from fastapi import APIRouter, Depends, status

from models.genre import Genre  

from schemas.genre import GenreCreate, GenreResponses

from services.dependencies import get_catalog_service, get_genre_service

router = APIRouter (
    prefix = "/genre",
    tags = ["genre"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_genre(genre: GenreCreate, get_genre_service = Depends(get_genre_service)):
    new_genre = Genre(name= genre.name)
    
    get_genre_service.add_genre(new_genre)
    return {"message": "Genre added successfully!"}

@router.delete("/{name}")
def remove_genre(name: str, catalog_service = Depends(get_catalog_service)):
    catalog_service.remove_genre(name)
    return {"message": "Genre removed successfully!"}
    
@router.get("/", response_model=list[GenreResponses])
def get_genres(get_genre_service = Depends(get_genre_service)):
    return get_genre_service.get_genres()