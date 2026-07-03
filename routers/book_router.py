from fastapi import APIRouter, Depends, status

from models.book import Book

from schemas.book import BookCreate, BookFilter, BookListResponse

from services.dependencies import library_service

router = APIRouter (
    prefix = "/books",
    tags = ["book"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate):
    new_book = Book(
        title = book.title,
        author = book.author,
        year = book.year,
        genre_id = book.genre_id
    )

    library_service.add_book(new_book)
    return {"message": "Book added successfully!"}

@router.delete("/{title}")
def remove_book(title: str):
    library_service.remove_book(title)
    return {"message": "Book removed successfully!"}

@router.get("/", response_model=BookListResponse)
def get_books(filters: BookFilter = Depends()):
    return library_service.get_books_list(filters)