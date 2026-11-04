class UserTeamKeyPostgreSQL_Exception(Exception):
    pass


class UserTeamKeyAdditionException(UserTeamKeyPostgreSQL_Exception):
    def __init__(self, message: str = "Error adding user teams key") -> None:
        self.message = message
        super().__init__(self.message)


class UserTeamKeyRetrievalException(UserTeamKeyPostgreSQL_Exception):
    def __init__(self, message: str = "Error retrieving user teams keys") -> None:
        self.message = message
        super().__init__(self.message)


class UserTeamKeyUpdateException(UserTeamKeyPostgreSQL_Exception):
    def __init__(self, message: str = "Error updating user teams key") -> None:
        self.message = message
        super().__init__(self.message)


class UserTeamKeyRemovalException(UserTeamKeyPostgreSQL_Exception):
    def __init__(self, message: str = "Error removing user teams key") -> None:
        self.message = message
        super().__init__(self.message)
