class TeamPostgreSQL_Exception(Exception):
    pass


class TeamMemberAdditionException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Error adding member to team"):
        self.message = message
        super().__init__(self.message)


class TeamMemberRetrievalException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Error retrieving team members"):
        self.message = message
        super().__init__(self.message)


class TeamMemberRoleUpdateException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Error updating team member role"):
        self.message = message
        super().__init__(self.message)


class TeamMemberRemovalException(TeamPostgreSQL_Exception):
    def __init__(self, message: str = "Error removing member from team"):
        self.message = message
        super().__init__(self.message)
