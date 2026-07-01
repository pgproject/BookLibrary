from fastapi import APIRouter, Depends, HTTPException, status

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

    can_add_book = library_service.add_book(new_book)
    if can_add_book:
        return {"message": "Book added successfully!"}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Genre not found. Please add the genre first before adding the book."
    )    

@router.delete("/{title}")
def remove_book(title: str):
    success = library_service.remove_book(title)
    if success:
        return {"message": "Book removed successfully!"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found!"
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