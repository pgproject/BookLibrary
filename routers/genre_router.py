from fastapi import APIRouter, HTTPException, status

from exceptions.genre_exceptions import GenreAlreadyExistsException, GenreIsUsedException, GenreNotFoundException
from models.genre import Genre  

from schemas.genre import GenreCreate
from schemas.genre import GenreResponses

from services.dependencies import genre_service
from services.dependencies import catalog_service

router = APIRouter (
    prefix = "/genre",
    tags = ["genre"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_genre(genre: GenreCreate):
    new_genre = Genre(name= genre.name)
    try:
        genre_service.add_genre(new_genre)
        return {"message": "Genre added successfully!"}

    except GenreAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{name}")
def remove_genre(name: str):
    try:
        catalog_service.remove_genre(name)
        return {"message": "Genre removed successfully!"}
    except GenreNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except GenreIsUsedException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
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