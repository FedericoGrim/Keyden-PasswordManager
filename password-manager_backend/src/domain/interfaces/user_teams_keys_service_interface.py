import uuid
from abc import ABC, abstractmethod

from domain.entities.user_teams_keys import UserTeamKey


@abstractmethod
class IUserTeamKeyService(ABC):
    @abstractmethod
    def add_key(self, new_key: UserTeamKey) -> UserTeamKey:
        pass

    @abstractmethod
    def get_key_by_id(self, key_id: uuid.UUID) -> UserTeamKey:
        pass

    @abstractmethod
    def get_keys_by_team_id(self, team_id: uuid.UUID) -> list[UserTeamKey]:
        pass

    @abstractmethod
    def get_keys_by_user_id(self, user_id: uuid.UUID) -> list[UserTeamKey]:
        pass

    @abstractmethod
    def update_key(self, new_key_data: UserTeamKey) -> UserTeamKey:
        pass

    @abstractmethod
    def remove_key(self, user_id: uuid.UUID, team_id: uuid.UUID) -> dict[str, str]:
        pass
