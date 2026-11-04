from application.dto.categories_dto import (
    CategoryDTO,
    CreateCategoryDTO,
    UpdateCategoryDTO,
)
from application.exceptions.categories_use_case_exceptions import (
    CategoryDeletionException,
    CategoryRetrievalException,
    CategoryUpdateException,
    CreateCategoryException,
)

from domain.interfaces.icategories import ICategoriesService

import uuid
from domain.entities.categories import Category


class CreateCategoriesUseCase:
    def __init__(self, CategoriesRepository: ICategoriesService) -> None:
        self.CategoriesRepository = CategoriesRepository

    def execute(
        self, category: CreateCategoryDTO, user_interactor_id: uuid.UUID
    ) -> Category:
        try:
            category_entity = category.to_entity()
            result = self.CategoriesRepository.CreateCategory(category_entity)

            return result

        except Exception as e:
            raise CreateCategoryException(str(e)) from e


class GetAllCategoriesByTeamIdUseCase:
    def __init__(self, CategoriesRepository: ICategoriesService) -> None:
        self.CategoriesRepository = CategoriesRepository

    def execute(self, teamId: uuid.UUID) -> list[CategoryDTO]:
        try:
            categories = self.CategoriesRepository.GetAllCategoriesByTeamId(teamId)
            return [
                CategoryDTO(
                    id=uuid.UUID(str(category.id)),
                    team_id=uuid.UUID(str(category.team_id)),
                    name=str(category.name),
                )
                for category in categories
            ]
        except Exception as e:
            raise CategoryRetrievalException(str(e)) from e


class UpdateCategoryByIdUseCase:
    def __init__(self, CategoriesRepository: ICategoriesService) -> None:
        self.CategoriesRepository = CategoriesRepository

    def execute(
        self,
        categoryId: uuid.UUID,
        new_category: UpdateCategoryDTO,
        user_interactor_id: uuid.UUID,
    ) -> CategoryDTO:
        try:
            result = self.CategoriesRepository.UpdateCategoryById(
                categoryId, new_category.to_entity()
            )

            return CategoryDTO(
                id=uuid.UUID(str(result.id)),
                team_id=uuid.UUID(str(result.team_id)),
                name=str(result.name),
            )

        except Exception as e:
            raise CategoryUpdateException(str(e)) from e


class DeleteCategoryByIdUseCase:
    def __init__(self, CategoriesRepository: ICategoriesService) -> None:
        self.CategoriesRepository = CategoriesRepository

    def execute(self, categoryId: uuid.UUID, user_interactor_id: uuid.UUID) -> bool:
        try:
            result = self.CategoriesRepository.DeleteCategoryById(categoryId)

            return result
        except Exception as e:
            raise CategoryDeletionException(str(e)) from e
