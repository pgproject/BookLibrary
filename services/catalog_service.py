from enums.remove_genre_results import RemoveGenreResults

class CatalogService:

    def __init__(
            self,
            genre_service,
            library_service
        ):
            self.genre_service = genre_service
            self.library_service = library_service

    def remove_genre(self, name: str) -> RemoveGenreResults:
            if self.library_service.genre_is_used(name):
                return RemoveGenreResults.GENRE_IS_USED
        
            removed = self.genre_service.remove_genre(name)
            if removed: 
                  return RemoveGenreResults.SUCCESS
            
            return RemoveGenreResults.NOT_FOUND