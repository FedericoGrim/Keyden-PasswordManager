import uuid
from abc import ABC, abstractmethod

from domain.entities.categories import Category

@abstractmethod
class ICategoriesService(ABC):
    @abstractmethod
    def CreateCategory(self, category: Category) -> Category:
        pass

    @abstractmethod
    def GetAllCategoriesByTeamId(self, teamId: uuid.UUID) -> list[Category]:
        pass

    @abstractmethod
    def UpdateCategoryById(self, categoryId: uuid.UUID, new_category: Category) -> Category:
        pass

    @abstractmethod
    def DeleteCategoryById(self, categoryId: uuid.UUID) -> bool:
        pass