from fastapi import  Request
from fastapi.responses import JSONResponse

from exceptions.book_exceptions import BookNotFoundException
from exceptions.genre_exceptions import GenreAlreadyExistsException, GenreIsUsedException, GenreNotFoundException

def book_not_found_exception_handler(
    request: Request, exc: BookNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

def genre_not_found_exception_handler(
    request: Request, exc: GenreNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

def genre_already_exists_exception_handler(
    request: Request, exc: GenreAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )

def genre_is_used_exception_handler(
    request: Request, exc: GenreIsUsedException):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )