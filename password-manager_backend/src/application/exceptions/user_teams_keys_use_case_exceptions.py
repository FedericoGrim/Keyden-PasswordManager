class UserTeamKeyAdditionException(Exception):
    def __init__(self, message: str = "Error adding user teams key") -> None:
        self.message = message
        super().__init__(self.message)


class UserTeamKeyRetrievalByIdException(Exception):
    def __init__(self, message: str = "Error retrieving user teams key by ID") -> None:
        self.message = message
        super().__init__(self.message)


class UserTeamKeysRetrievalByTeamIdException(Exception):
    def __init__(
        self, message: str = "Error retrieving user teams keys by Team ID"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class UserTeamKeysRetrievalByUserIdException(Exception):
    def __init__(
        self, message: str = "Error retrieving user teams keys by User ID"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class UserTeamKeyUpdateException(Exception):
    def __init__(self, message: str = "Error updating user teams key") -> None:
        self.message = message
        super().__init__(self.message)


class UserTeamKeyRemovalException(Exception):
    def __init__(self, message: str = "Error removing user teams key") -> None:
        self.message = message
        super().__init__(self.message)
