from pydantic import BaseModel, UUID4

from domain.entities.sub_account_categories import SubAccountCategories


class SubAccountCategoriesDTO(BaseModel):
    sub_account_id: UUID4
    category_id: UUID4

    def to_entity(self) -> SubAccountCategories:
        return SubAccountCategories(
            sub_account_id=self.sub_account_id, category_id=self.category_id
        )


class CreateSubAccountCategoryDTO(BaseModel):
    sub_account_id: UUID4
    category_id: UUID4

    def to_entity(self) -> SubAccountCategories:
        return SubAccountCategories(
            sub_account_id=self.sub_account_id, category_id=self.category_id
        )
