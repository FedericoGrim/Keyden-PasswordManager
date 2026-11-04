class UserCreationException(Exception):
    def __init__(self, message: str = "Error creating user.") -> None:
        self.message = message
        super().__init__(self.message)


class UserRetrievalException(Exception):
    def __init__(self, message: str = "Error retrieving user.") -> None:
        self.message = message
        super().__init__(self.message)


class UserUpdateException(Exception):
    def __init__(self, message: str = "Error updating user.") -> None:
        self.message = message
        super().__init__(self.message)


class UserDeletionException(Exception):
    def __init__(self, message: str = "Error deleting user.") -> None:
        self.message = message
        super().__init__(self.message)
