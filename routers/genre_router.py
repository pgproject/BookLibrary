from fastapi import APIRouter

from models.genre import Genre  

from schemas.genre import GenreCreate
from schemas.genre import GenreResponses

from enums.remove_genre_results import RemoveGenreResults

from services.dependencies import genre_service
from services.dependencies import catalog_service

router = APIRouter (
    prefix = "/genre",
    tags = ["genre"]
)

@router.post("/")
def add_genre(genre: GenreCreate):
    new_genre = Genre(name= genre.name)

    added = genre_service.add_genre(new_genre)
    if added:
        return {"message": "Genre added successfully!"}

    return {"message": "Genre is exists, you can't add it!"}


@router.delete("/{name}")
def remove_genre(name: str):
    remove_result = catalog_service.remove_genre(name)
    
    if remove_result == RemoveGenreResults.SUCCESS:
        return {"message": "Genre removed successfully!"}
    elif remove_result == RemoveGenreResults.NOT_FOUND:
        return {"message": "Genre not found."}
    return {"message": "Genre is used."}
    
@router.get("/", response_model=list[GenreResponses])
def get_genres():
    return genre_service.get_genres()