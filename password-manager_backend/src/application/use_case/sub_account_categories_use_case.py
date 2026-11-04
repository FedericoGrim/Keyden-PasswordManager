import uuid

from application.exceptions.sub_account_categories_use_case_exceptions import *
from application.dto.sub_account_categories_dto import *

from domain.interfaces.isub_account_categories_service import (
    ISubAccountCategoriesService,
)


class CreateSubAccountCategoryUseCase:
    def __init__(self, SubAccountCategoriesRepository: ISubAccountCategoriesService):
        self.SubAccountCategoriesRepository = SubAccountCategoriesRepository

    def execute(self, new_subacc_category: CreateSubAccountCategoryDTO):
        try:
            result = self.SubAccountCategoriesRepository.CreateSubAccountCategory(
                new_subacc_category.to_entity()
            )

            return result

        except Exception as e:
            raise CreateSubAccountCategoryException(str(e)) from e


class GetAllCategoriesBySubAccountIdUseCase:
    def __init__(self, SubAccountCategoriesRepository: ISubAccountCategoriesService):
        self.SubAccountCategoriesRepository = SubAccountCategoriesRepository

    def execute(self, subaccountId: uuid.UUID) -> list[SubAccountCategoriesDTO]:
        try:
            subacc_categories = (
                self.SubAccountCategoriesRepository.GetAllCategoriesBySubAccountId(
                    subaccountId
                )
            )
            return [
                SubAccountCategoriesDTO(
                    sub_account_id=uuid.UUID(str(entity.sub_account_id)),
                    category_id=uuid.UUID(str(entity.category_id)),
                )
                for entity in subacc_categories
            ]
        except Exception as e:
            raise SubAccountCategoryRetrievalException(str(e)) from e


class DeleteSubAccountCategoryUseCase:
    def __init__(self, SubAccountCategoriesRepository: ISubAccountCategoriesService):
        self.SubAccountCategoriesRepository = SubAccountCategoriesRepository

    def execute(self, subacc_category: SubAccountCategoriesDTO) -> bool:
        try:
            return self.SubAccountCategoriesRepository.DeleteSubAccountCategory(
                subacc_category.to_entity()
            )
        except Exception as e:
            raise SubAccountCategoryDeletionException(str(e)) from e
