class TeamCreationException(Exception):
    def __init__(self, message: str = "Error creating team") -> None:
        self.message = message
        super().__init__(self.message)


class TeamRetrievalByIdException(Exception):
    def __init__(self, message: str = "Error retrieving team by ID") -> None:
        self.message = message
        super().__init__(self.message)


class TeamsRetrievalByUserIdException(Exception):
    def __init__(self, message: str = "Error retrieving teams by User ID") -> None:
        self.message = message
        super().__init__(self.message)


class TeamUpdateException(Exception):
    def __init__(self, message: str = "Error updating team") -> None:
        self.message = message
        super().__init__(self.message)


class TeamDeleteException(Exception):
    def __init__(self, message: str = "Error deleting team") -> None:
        self.message = message
        super().__init__(self.message)


class TeamNotFoundException(Exception):
    def __init__(self, message: str = "Team not found") -> None:
        self.message = message
        super().__init__(self.message)


class TeamAlreadyExistsException(Exception):
    def __init__(self, message: str = "Team already exists") -> None:
        self.message = message
        super().__init__(self.message)
