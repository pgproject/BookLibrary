from fastapi import APIRouter, HTTPException, status

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

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_genre(genre: GenreCreate):
    new_genre = Genre(name= genre.name)

    added = genre_service.add_genre(new_genre)
    if added:
        return {"message": "Genre added successfully!"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Genre already exists!"
    )


@router.delete("/{name}")
def remove_genre(name: str):
    remove_result = catalog_service.remove_genre(name)
    
    if remove_result == RemoveGenreResults.SUCCESS:
        return {"message": "Genre removed successfully!"}
    elif remove_result == RemoveGenreResults.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found."
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Genre is used."
    )

@router.get("/", response_model=list[GenreResponses])
def get_genres():
    genres = genre_service.get_genres()
    if not genres:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No genres found."
        )
    return genres