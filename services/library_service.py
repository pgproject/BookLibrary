from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import ColumnElement

from database import SessionLocal

from exceptions.book_exceptions import BookNotFoundException
from exceptions.genre_exceptions import GenreNotFoundException
from models.book import Book
from models.genre import Genre

from schemas.book import (
    BookFilter, 
    BookDetailsResponse, 
    BookListResponse
)

from enums.book_enums import BookSort 

import math

class LibraryService:
    def __init__(self, session, genre_service):
        self.session = session
        self.genre_service = genre_service

    def add_book(self, book):

        genre = self.session.get(Genre, book.genre_id)

        if not genre:
            raise GenreNotFoundException()

        self.session.add(book)
        self.session.commit()
       

    def remove_book(self, title: str):
        book = self.session.scalar(
            select(Book)
            .where(Book.title == title)
        )
        if not book:
            raise BookNotFoundException()

        self.session.delete(book)
        self.session.commit()

    def genre_is_used(self, name: str) -> bool:
        book = self.session.scalar(
            select(Book)
            .join(Book.genre)
            .where(Genre.name == name)
        )

        return book is not None

    def get_books_list(self, filters: BookFilter) -> BookListResponse:
        
        conditions = self._create_conditions(filters)

        book_list = BookListResponse(
            details=self._get_books_details(filters, conditions),
            items=self._get_books(filters, conditions)
        )

        return book_list

    def _get_books(self, filters: BookFilter, conditions: list[ColumnElement]):
        
        query = (
            select(Book)
            .options(joinedload(Book.genre))
            .where(*conditions)
        )

        sort_columns = {
            BookSort.title: Book.title,
            BookSort.author: Book.author,
            BookSort.year: Book.year,
        }
        
        column = sort_columns[filters.sort]
       
        if filters.descending:
            query = query.order_by(column.desc())
        else:                 
            query = query.order_by(column)

        query = (
            query
            .limit(filters.page_size)
            .offset((filters.page - 1) * filters.page_size)
        )

        return self.session.scalars(query).all()

    def _get_books_details(self, filters: BookFilter, conditions: list[ColumnElement]) -> BookDetailsResponse:
        
        query = (
            select(func.count())
            .select_from(Book)
            .where(*conditions)
        )
        
        count = self.session.scalar(query)
        amount_of_pages = math.ceil(count / filters.page_size)

        return BookDetailsResponse(
            total=count, 
            pages=amount_of_pages,
            page=filters.page,
            page_size=filters.page_size
        )


    def _create_conditions(self, filters: BookFilter) -> list[ColumnElement]:
        conditions = []

        if filters.title:
            conditions.append(Book.title.ilike(f"%{filters.title}%"))
        
        if filters.author:
            conditions.append(Book.author.ilike(f"%{filters.author}%"))

        if filters.year_from:
            conditions.append(Book.year >= filters.year_from)

        if filters.year_to:
            conditions.append(Book.year <= filters.year_to)

        if filters.genre:
            genre_id = self.genre_service.get_genre_id(filters.genre)

            conditions.append(Book.genre_id == genre_id)

        return conditions
