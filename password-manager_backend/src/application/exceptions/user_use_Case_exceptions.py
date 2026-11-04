class UserCreationException(Exception):
    def __init__(self, message: str = "Error creating user."):
        self.message = message
        super().__init__(self.message)


class UserRetrievalException(Exception):
    def __init__(self, message: str = "Error retrieving user."):
        self.message = message
        super().__init__(self.message)


class UserUpdateException(Exception):
    def __init__(self, message: str = "Error updating user."):
        self.message = message
        super().__init__(self.message)


class UserDeletionException(Exception):
    def __init__(self, message: str = "Error deleting user."):
        self.message = message
        super().__init__(self.message)
