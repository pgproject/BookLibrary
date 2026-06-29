from enum import Enum

class RemoveGenreResults(Enum):
    SUCCESS = 1
    NOT_FOUND = 2
    GENRE_IS_USED = 3