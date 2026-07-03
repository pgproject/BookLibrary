from fastapi import FastAPI                                                                                                                                                                                                                                                                          

from database import Base, engine

from exceptions.book_exceptions import BookNotFoundException
from exceptions.genre_exceptions import GenreAlreadyExistsException, GenreIsUsedException, GenreNotFoundException

from exceptions.handlers import (
    book_not_found_exception_handler, 
    genre_already_exists_exception_handler, 
    genre_is_used_exception_handler, 
    genre_not_found_exception_handler
)

from routers.genre_router import router as genres_router
from routers.book_router import router as books_router

Base.metadata.create_all(engine)

app = FastAPI()

app.add_exception_handler(BookNotFoundException, book_not_found_exception_handler)
app.add_exception_handler(GenreNotFoundException, genre_not_found_exception_handler)
app.add_exception_handler(GenreAlreadyExistsException, genre_already_exists_exception_handler)
app.add_exception_handler(GenreIsUsedException, genre_is_used_exception_handler)

app.include_router(genres_router)
app.include_router(books_router)


@app.get("/")
def root():
    return {"message": "Hello, World!"}