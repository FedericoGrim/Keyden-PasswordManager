class UserFavoriteAdditionException(Exception):
    def __init__(self, message: str = "Error adding favorite") -> None:
        self.message = message
        super().__init__(self.message)


class UserFavoriteRetrievalException(Exception):
    def __init__(self, message: str = "Error retrieving favorites") -> None:
        self.message = message
        super().__init__(self.message)


class UserFavoriteRemovalException(Exception):
    def __init__(self, message: str = "Error removing favorite") -> None:
        self.message = message
        super().__init__(self.message)
