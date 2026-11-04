import uuid
from abc import ABC, abstractmethod

from domain.entities.team_perm_level import TeamPermLevel


@abstractmethod
class ITeamPermLevelService(ABC):
    @abstractmethod
    def CreateTeamPermLevel(self, perm_level: TeamPermLevel) -> TeamPermLevel:
        pass

    @abstractmethod
    def GetTeamPermLevelById(self, perm_level_id: uuid.UUID) -> TeamPermLevel:
        pass

    @abstractmethod
    def GetAllTeamPermLevelsByTeamId(self, teamId: uuid.UUID) -> list[TeamPermLevel]:
        pass

    @abstractmethod
    def UpdateTeamPermLevelById(
        self, perm_level_id: uuid.UUID, new_perm_level: TeamPermLevel
    ) -> TeamPermLevel:
        pass

    @abstractmethod
    def DeleteTeamPermLevelById(self, perm_level_id: uuid.UUID) -> bool:
        pass
