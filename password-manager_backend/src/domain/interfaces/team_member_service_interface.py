import uuid
from abc import ABC, abstractmethod

from domain.entities.team_member import TeamMember


@abstractmethod
class ITeamMembersService(ABC):
    @abstractmethod
    def add_member_to_team(self, new_member: TeamMember) -> TeamMember:
        pass

    @abstractmethod
    def get_team_member_by_id(self, member_id: uuid.UUID) -> TeamMember:
        pass

    @abstractmethod
    def get_team_member_by_user_and_team(
        self, user_id: uuid.UUID, team_id: uuid.UUID
    ) -> TeamMember:
        pass

    @abstractmethod
    def get_members_by_team_id(self, team_id: uuid.UUID) -> list[TeamMember]:
        pass

    @abstractmethod
    def update_member_role(self, new_user_data: TeamMember) -> TeamMember:
        pass

    @abstractmethod
    def remove_member_from_team(
        self, member_id: uuid.UUID, team_id: uuid.UUID
    ) -> dict[str, str]:
        pass
