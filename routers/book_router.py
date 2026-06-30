from fastapi import APIRouter, Depends

from models.book import Book

from schemas.book import BookCreate
from schemas.book import BookResponse
from schemas.book import BookFilter
from schemas.book import BookListResponse

from services.dependencies import library_service

router = APIRouter (
    prefix = "/books",
    tags = ["book"]
)

@router.post("/")
def add_book(book: BookCreate):
    new_book = Book(
        title = book.title,
        author = book.author,
        year = book.year,
        genre_id = book.genre_id
    )

    can_add_book = library_service.add_book(new_book)
    if can_add_book:
        return {"message": "Book added successfully"}
    else:
        return {"message": "You can't add book"}

@router.delete("/{title}")
def remove_book(title: str):
    success = library_service.remove_book(title)
    if success:
        return {"message": "Book removed successfully!"}
    else:
        return {"message": "Book not found!"}
    
@router.get("/", response_model=BookListResponse)
def get_total_books(filters: BookFilter = Depends()):
    return library_service.get_books_list(filters)