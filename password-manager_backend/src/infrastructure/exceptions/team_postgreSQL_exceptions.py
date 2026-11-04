class TeamPostgreSQL_Exception(Exception):
    pass


class TeamAlreadyExistsException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Team member already exists in the team") -> None:
        self.message = message
        super().__init__(self.message)


class TeamCreationFailedException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Team member creation failed") -> None:
        self.message = message
        super().__init__(self.message)


class GetTeamByIdRetrivalException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Error retrieving team by ID") -> None:
        self.message = message
        super().__init__(self.message)


class GetTeamByIdNotFoundException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "No team found for the given team ID") -> None:
        self.message = message
        super().__init__(self.message)


class GetTeamsByUserIdNotFoundException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "No teams found for the given user ID") -> None:
        self.message = message
        super().__init__(self.message)


class TeamRetrievalException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Error retrieving teams") -> None:
        self.message = message
        super().__init__(self.message)


class TeamNotFoundException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Team not found") -> None:
        self.message = message
        super().__init__(self.message)


class TeamUpdateException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Error updating team") -> None:
        self.message = message
        super().__init__(self.message)


class TeamDeleteException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Error deleting team") -> None:
        self.message = message
        super().__init__(self.message)
