class CreateTeamPermLevelException(Exception):
    def __init__(self, message: str = "Failed to create team perm level."):
        self.message = message
        super().__init__(self.message)


class TeamPermLevelRetrievalException(Exception):
    def __init__(self, message: str = "Failed to retrieve team perm levels."):
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
