import uuid
from abc import ABC, abstractmethod

from domain.entities.sub_account_history import SubAccountHistory

@abstractmethod
class ISubAccountHistoryService(ABC):
    @abstractmethod
    def CreateHistoryEntry(self, entry: SubAccountHistory) -> SubAccountHistory:
        pass

    @abstractmethod
    def GetHistoryBySubAccountId(self, sub_account_id: uuid.UUID) -> list[SubAccountHistory]:
        pass

    @abstractmethod
    def GetHistoryByTeamId(self, team_id: uuid.UUID) -> list[SubAccountHistory]:
        pass

    @abstractmethod
    def UpdateHistoryDek(self, history_id: uuid.UUID, dek_wrapped: str) -> SubAccountHistory:
        pass
