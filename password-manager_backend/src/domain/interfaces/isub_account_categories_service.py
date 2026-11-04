import uuid
from abc import ABC, abstractmethod

from domain.entities.sub_account_categories import SubAccountCategories


@abstractmethod
class ISubAccountCategoriesService(ABC):
    @abstractmethod
    def CreateSubAccountCategory(
        self, new_subacc_category: SubAccountCategories
    ) -> SubAccountCategories:
        pass

    @abstractmethod
    def GetAllCategoriesBySubAccountId(
        self, subaccountId: uuid.UUID
    ) -> list[SubAccountCategories]:
        pass

    @abstractmethod
    def DeleteSubAccountCategory(self, subacc_category: SubAccountCategories) -> bool:
        pass
