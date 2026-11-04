class TeamPermLevelAlreadyExistsException(Exception):
    def __init__(
        self,
        message: str = "Team perm level with the same name already exists for this team.",
    ):
        self.message = message
        super().__init__(self.message)


class TeamPermLevelCreationFailedException(Exception):
    def __init__(self, message: str = "Failed to create team perm level."):
        self.message = message
        super().__init__(self.message)


class GetAllTeamPermLevelsByTeamIdNotFoundException(Exception):
    def __init__(self, message: str = "No perm levels found for the given team ID."):
        self.message = message
        super().__init__(self.message)


class TeamPermLevelRetrievalException(Exception):
    def __init__(self, message: str = "Failed to retrieve team perm levels."):
        self.message = message
        super().__init__(self.message)


class TeamPermLevelNotFoundException(Exception):
    def __init__(self, message: str = "Team perm level not found."):
        self.message = message
        super().__init__(self.message)


class TeamPermLevelUpdateException(Exception):
    def __init__(self, message: str = "Failed to update team perm level."):
        self.message = message
        super().__init__(self.message)


class TeamPermLevelDeletionException(Exception):
    def __init__(self, message: str = "Failed to delete team perm level."):
        self.message = message
        super().__init__(self.message)
