from fastapi import APIRouter, Depends, HTTPException, status

from exceptions.book_exceptions import BookNotFoundException
from exceptions.genre_exceptions import GenreNotFoundException
from models.book import Book

from schemas.book import BookCreate, BookFilter, BookListResponse

from services.dependencies import library_service

router = APIRouter (
    prefix = "/books",
    tags = ["book"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate):
    try:
        new_book = Book(
            title = book.title,
            author = book.author,
            year = book.year,
            genre_id = book.genre_id
        )

        library_service.add_book(new_book)
        return {"message": "Book added successfully!"}
    except GenreNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{title}")
def remove_book(title: str):
    try:
        library_service.remove_book(title)
        return {"message": "Book removed successfully!"}

    except BookNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/", response_model=BookListResponse)
def get_books(filters: BookFilter = Depends()):
    books_list = library_service.get_books_list(filters)

    if books_list.details.total == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books found with the given filters."
        )
    
    return books_list