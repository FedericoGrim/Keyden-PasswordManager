class UserFavoritesPostgreSQL_Exception(Exception):
    pass


class UserFavoriteAdditionException(UserFavoritesPostgreSQL_Exception):
    def __init__(self, message: str = "Error adding favorite"):
        self.message = message
        super().__init__(self.message)


class UserFavoriteRetrievalException(UserFavoritesPostgreSQL_Exception):
    def __init__(self, message: str = "Error retrieving favorites"):
        self.message = message
        super().__init__(self.message)


class UserFavoriteRemovalException(UserFavoritesPostgreSQL_Exception):
    def __init__(self, message: str = "Error removing favorite"):
        self.message = message
        super().__init__(self.message)
