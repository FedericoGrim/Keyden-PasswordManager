import uuid
from abc import ABC, abstractmethod

from domain.entities.sub_account import SubAccount

@abstractmethod
class ISubAccountService(ABC):
    @abstractmethod
    def CreateSubAccount(self, sub_account: SubAccount) -> SubAccount:
        pass
    
    @abstractmethod
    def GetSubAccountById(self, sub_account_id: uuid.UUID) -> SubAccount:
        pass

    @abstractmethod
    def GetAllSubAccountsByTeamId(self, team_id: uuid.UUID) -> list[SubAccount]:
        pass

    @abstractmethod
    def UpdateSubAccountById(self, new_subaccount: SubAccount) -> SubAccount:
        pass

    @abstractmethod
    def DeleteSubAccountById(self, sub_account_id: uuid.UUID) -> dict[str, str]:
        pass

    @abstractmethod
    def UpdateSubAccountDek(self, sub_account_id: uuid.UUID, dek_wrapped: str) -> SubAccount:
        pass