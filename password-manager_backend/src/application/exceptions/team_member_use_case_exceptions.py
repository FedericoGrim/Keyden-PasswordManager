class TeamMemberAdditionException(Exception):
    def __init__(self, message: str = "Error adding member to team") -> None:
        self.message = message
        super().__init__(self.message)


class TeamMembersRetrievalByTeamIdException(Exception):
    def __init__(
        self, message: str = "Error retrieving team members by Team ID"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class TeamMemberRetrievalByIdException(Exception):
    def __init__(self, message: str = "Error retrieving team member by ID") -> None:
        self.message = message
        super().__init__(self.message)


class TeamsRetrievalByMemberIdException(Exception):
    def __init__(self, message: str = "Error retrieving teams by Member ID") -> None:
        self.message = message
        super().__init__(self.message)


class TeamMemberRoleUpdateException(Exception):
    def __init__(self, message: str = "Error updating team member role") -> None:
        self.message = message
        super().__init__(self.message)


class TeamMemberRemovalException(Exception):
    def __init__(self, message: str = "Error removing member from team") -> None:
        self.message = message
        super().__init__(self.message)
