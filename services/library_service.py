from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import SessionLocal

from models.book import Book
from models.genre import Genre

from schemas.book import BookFilter

from enums.book_enums import BookSort 

class LibraryService:
    def __init__(self, genre_service):
        self.session = SessionLocal()
        self.genre_service = genre_service

    def add_book(self, book) -> bool:
        genre = self.session.get(Genre, book.genre_id)

        if genre:
            self.session.add(book)
            self.session.commit()
            return True
        else:
            return False

    def remove_book(self, title: str):
        book = self.session.scalar(
            select(Book)
            .where(Book.title == title)
        )
        if book:
            self.session.delete(book)
            self.session.commit()
            return True
        return False

    def genre_is_used(self, name: str) -> bool:
        book = self.session.scalar(
            select(Book)
            .join(Book.genre)
            .where(Genre.name == name)
        )

        if book:
            return True
        
        return False

    def get_books(self, filters: BookFilter):
        
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
        
        column = sort_columns.get(filters.sort)
      
       
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