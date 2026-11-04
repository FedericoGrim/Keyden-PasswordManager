from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.sub_account_categories_postgresql_exceptions import (
    GetAllCategoriesBySubAccountIdNotFoundException,
    SubAccountCategoryAlreadyExistsException,
    SubAccountCategoryCreationFailedException,
    SubAccountCategoryDeletionFailedException,
    SubAccountCategoryNotFoundException,
    SubAccountCategoryRetrievalException,
)

from domain.interfaces.isub_account_categories_service import (
    ISubAccountCategoriesService,
)
from domain.entities.sub_account_categories import SubAccountCategories
from infrastructure.databases.models.sub_account_categories_model import (
    SubAccountCategoriesModel,
)


def _to_domain(model: SubAccountCategoriesModel) -> SubAccountCategories:
    return SubAccountCategories(
        id=model.id,
        sub_account_id=model.sub_account_id,
        category_id=model.category_id,
    )


class SubAccountCategoriesService(ISubAccountCategoriesService):
    def __init__(self, db: Session) -> None:
        self.Db = db

    def CreateSubAccountCategory(
        self, new_subacc_category: SubAccountCategories
    ) -> SubAccountCategories:
        try:
            subacc_category_model = SubAccountCategoriesModel(
                sub_account_id=new_subacc_category.sub_account_id,
                category_id=new_subacc_category.category_id,
            )

            self.Db.add(subacc_category_model)
            self.Db.flush()
            self.Db.refresh(subacc_category_model)
            return _to_domain(subacc_category_model)

        except IntegrityError:
            raise SubAccountCategoryAlreadyExistsException(
                "SubAccountCategory with the same subaccount and category already exists."  # noqa: E501
            )

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCategoryCreationFailedException(
                "Failed to create subacc category."
            )

    def GetAllCategoriesBySubAccountId(
        self, subaccountId: uuid.UUID
    ) -> list[SubAccountCategories]:
        try:
            subacc_category_models: list[SubAccountCategoriesModel] = (
                self.Db.query(SubAccountCategoriesModel)
                .filter(SubAccountCategoriesModel.sub_account_id == subaccountId)
                .all()
            )
            if not subacc_category_models:
                raise GetAllCategoriesBySubAccountIdNotFoundException(
                    "No categories found for the given subaccount ID."
                )
            return [
                _to_domain(subacc_category_model)
                for subacc_category_model in subacc_category_models
            ]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCategoryRetrievalException(
                "Failed to retrieve subacc categories."
            )

    def DeleteSubAccountCategory(self, subacc_category: SubAccountCategories) -> bool:
        try:
            subacc_category_model = (
                self.Db.query(SubAccountCategoriesModel)
                .filter(
                    SubAccountCategoriesModel.sub_account_id
                    == subacc_category.sub_account_id,
                    SubAccountCategoriesModel.category_id
                    == subacc_category.category_id,
                )
                .first()
            )

            if not subacc_category_model:
                raise SubAccountCategoryNotFoundException(
                    "SubAccountCategory not found."
                )

            self.Db.delete(subacc_category_model)
            self.Db.flush()
            return True

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCategoryDeletionFailedException(
                "Failed to delete subacc category."
            )
