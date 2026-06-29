from enum import Enum

class BookSort(str, Enum):
    title = "title"
    author = "author"
    year = "year"