import uuid
from abc import ABC, abstractmethod

from domain.entities.team import Team


@abstractmethod
class ITeamService(ABC):
    @abstractmethod
    def CreateTeam(self, new_team: Team) -> Team:
        pass

    @abstractmethod
    def GetTeamById(self, team_id: uuid.UUID) -> Team:
        pass

    @abstractmethod
    def GetTeamsByUserId(self, user_id: uuid.UUID) -> list[Team]:
        pass

    @abstractmethod
    def UpdateTeamById(self, new_team: Team) -> Team:
        pass

    @abstractmethod
    def DeleteTeamById(self, team_id: uuid.UUID) -> dict[str, str]:
        pass
