class UserAlreadyExistsException(Exception):
    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)


class UserCreationFailedException(Exception):
    def __init__(self, message: str = "User creation failed"):
        self.message = message
        super().__init__(self.message)


class GetUserByIdRetrivalException(Exception):
    def __init__(self, message: str = "Error retrieving local users by ID"):
        self.message = message
        super().__init__(self.message)


class GetUserByIdNotFoundException(Exception):
    def __init__(
        self, message: str = "No local users found for the given main user ID"
    ):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, message: str = "Local user not found"):
        self.message = message
        super().__init__(self.message)


class UserUpdateFailedException(Exception):
    def __init__(self, message: str = "Error updating local user"):
        self.message = message
        super().__init__(self.message)


class UserDeleteException(Exception):
    def __init__(self, message: str = "Error deleting local user"):
        self.message = message
        super().__init__(self.message)
