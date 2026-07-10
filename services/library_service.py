from sqlalchemy.sql.elements import ColumnElement

from exceptions.book_exceptions import BookNotFoundException
from exceptions.genre_exceptions import GenreNotFoundException

from models.book import Book

from repositories.library_repositories import LibraryRepository
from schemas.book import (
    BookFilter, 
    BookDetailsResponse, 
    BookListResponse
)
from services.genre_service import GenreService

import math

class LibraryService:
    def __init__(self,
                genre_service: GenreService,
                library_repository: LibraryRepository):
        self.genre_service = genre_service
        self.library_repository = library_repository
        

    def add_book(self, book: Book):

        self.genre_service.get_genre_by_id(book.genre_id)
        self.library_repository.add_book(book)

    def remove_book(self, title: str):
        book = self.library_repository.find_book_by_title(title)
        if not book:
            raise BookNotFoundException()

        self.library_repository.remove_book(book)

    def genre_is_used(self, name: str) -> bool:
        return self.library_repository.exists_book_with_genre_name(name)
    
    def get_books_list(self, filters: BookFilter) -> BookListResponse:

        book_list = BookListResponse(
            details=self._get_books_details(filters),
            items=self.library_repository.find_books(filters)
        )

        return book_list

    def _get_books_details(self, filters: BookFilter) -> BookDetailsResponse:
        
        amount_of_books = self.library_repository.count_books(filters)
        amount_of_pages = math.ceil(amount_of_books / filters.page_size)

        return BookDetailsResponse(
            total=amount_of_books, 
            pages=amount_of_pages,
            page=filters.page,
            page_size=filters.page_size
        )