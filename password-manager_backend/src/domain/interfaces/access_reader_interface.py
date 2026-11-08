import uuid
from abc import ABC, abstractmethod
from typing import Optional


class IAccessReader(ABC):
    @abstractmethod
    def rank_in_team(self, user_id: uuid.UUID, team_id: uuid.UUID) -> Optional[int]:
        """Rank of the user's permission level in the team, None if not a member."""

    @abstractmethod
    def team_has_members(self, team_id: uuid.UUID) -> bool:
        pass

    @abstractmethod
    def team_of_sub_account(self, sub_account_id: uuid.UUID) -> Optional[uuid.UUID]:
        pass

    @abstractmethod
    def team_of_category(self, category_id: uuid.UUID) -> Optional[uuid.UUID]:
        pass

    @abstractmethod
    def team_of_perm_level(self, perm_level_id: uuid.UUID) -> Optional[uuid.UUID]:
        pass

    @abstractmethod
    def member_row(self, member_id: uuid.UUID) -> Optional[tuple[uuid.UUID, uuid.UUID]]:
        """(team_id, user_id) of a team_members row."""

    @abstractmethod
    def key_row(self, key_id: uuid.UUID) -> Optional[tuple[uuid.UUID, uuid.UUID]]:
        """(team_id, user_id) of a user_teams_keys row."""
