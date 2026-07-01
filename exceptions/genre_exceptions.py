class GenreAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("Genre already exists!")
    pass

class GenreIsUsedException(Exception):
    def __init__(self):
        super().__init__("Genre is used.")
    pass

class GenreNotFoundException(Exception):
    def __init__(self):
        super().__init__("Genre not found.")
    pass