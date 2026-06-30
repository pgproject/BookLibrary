from pydantic import BaseModel
from pydantic import ConfigDict

from enums.book_enums import BookSort

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    genre_id: int

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre_id: int
    
    model_config = ConfigDict(from_attributes=True)

class BookFilter(BaseModel):
    title: str | None = None
    author: str | None = None
    year_from: int | None = None
    year_to: int | None = None
    genre: str | None = None
    sort: BookSort = BookSort.title
    page: int = 1
    page_size: int = 20
    descending: bool = False


class BookDetailsResponse(BaseModel):
    total: int
    pages: int
    page: int
    page_size: int

class BookListResponse(BaseModel):
    details: BookDetailsResponse
    items: list[BookResponse]
