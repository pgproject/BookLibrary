from sqlalchemy import select, func
from sqlalchemy.sql import Select
from sqlalchemy.orm import Session, joinedload

from enums.book_enums import BookSort
from models.book import Book
from models.genre import Genre

from schemas.book import BookFilter

class LibraryRepository:
    
    _SORT_COLUMNS = {
        BookSort.title: Book.title,
        BookSort.author: Book.author,
        BookSort.year: Book.year,
    }

    def __init__(self, session: Session):
        self.session = session

    def add_book(self, new_book: Book):
        self.session.add(new_book)
        self.session.commit()

    def remove_book(self, book: Book):
        self.session.delete(book)
        self.session.commit()

    def find_book_by_title(self, title: str)-> Book | None:
        return self.session.scalar(
            select(Book)
            .where(Book.title == title)
        )
    
    def find_books(self, filters: BookFilter)-> list[Book]:
        query = select(Book).options(joinedload(Book.genre))

        query = self._build_query(query, filters)
        
        column = self._SORT_COLUMNS[filters.sort]
       
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
    
    def count_books(self, filters: BookFilter)-> int:
        query = (
            select(func.count())
            .select_from(Book)
        )
        query = self._build_query(query, filters)

        return self.session.scalar(query)
    
    def exists_book_with_genre_name(self, genre_name: str) -> bool: 
        book = self.session.scalar(
            select(Book)
            .join(Book.genre)
            .where(Genre.name == genre_name)
        )
        return book is not None
    
    def _build_query(self, query: Select, filters: BookFilter) -> Select:

        if filters.title:
            query = query.where(Book.title.ilike(f"%{filters.title}%"))
        
        if filters.author:
            query = query.where(Book.author.ilike(f"%{filters.author}%"))

        if filters.year_from:
            query = query.where(Book.year >= filters.year_from)

        if filters.year_to:
            query = query.where(Book.year <= filters.year_to)

        if filters.genre:
            query = query.join(Book.genre)
            query = query.where(Genre.name == filters.genre)
        
        return query