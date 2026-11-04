class UserFavoritesPostgreSQL_Exception(Exception):
    pass


class UserFavoriteAdditionException(UserFavoritesPostgreSQL_Exception):
    def __init__(self, message: str = "Error adding favorite") -> None:
        self.message = message
        super().__init__(self.message)


class UserFavoriteRetrievalException(UserFavoritesPostgreSQL_Exception):
    def __init__(self, message: str = "Error retrieving favorites") -> None:
        self.message = message
        super().__init__(self.message)


class UserFavoriteRemovalException(UserFavoritesPostgreSQL_Exception):
    def __init__(self, message: str = "Error removing favorite") -> None:
        self.message = message
        super().__init__(self.message)
