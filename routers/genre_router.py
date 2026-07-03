from fastapi import APIRouter, HTTPException, status

from models.genre import Genre  

from schemas.genre import GenreCreate, GenreResponses

from services.dependencies import genre_service, catalog_service

router = APIRouter (
    prefix = "/genre",
    tags = ["genre"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_genre(genre: GenreCreate):
    new_genre = Genre(name= genre.name)
    
    genre_service.add_genre(new_genre)
    return {"message": "Genre added successfully!"}

@router.delete("/{name}")
def remove_genre(name: str):
    catalog_service.remove_genre(name)
    return {"message": "Genre removed successfully!"}
    
@router.get("/", response_model=list[GenreResponses])
def get_genres():
    return genre_service.get_genres()