from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.categories_postgresql_exceptions import *

from domain.interfaces.icategories import ICategoriesService
from domain.entities.categories import Category
from infrastructure.databases.models.categories_model import CategoriesModel


def _to_domain(model: CategoriesModel) -> Category:
    return Category(
        id=model.id,
        team_id=model.team_id,
        name=model.name,
    )


class CategoriesService(ICategoriesService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateCategory(self, category: Category) -> Category:
        try:
            category_model = CategoriesModel(
                team_id=category.team_id, name=category.name
            )

            self.Db.add(category_model)
            self.Db.flush()
            self.Db.refresh(category_model)
            return _to_domain(category_model)

        except IntegrityError:
            raise CategoryAlreadyExistsException(
                "Category with the same name already exists."
            )

        except Exception as e:
            logging.error(f"Error: {e}")
            raise CategoryCreationFailedException("Failed to create category.")

    def GetAllCategoriesByTeamId(self, teamId: uuid.UUID) -> list[Category]:
        try:
            category_models: list[CategoriesModel] = (
                self.Db.query(CategoriesModel)
                .filter(CategoriesModel.team_id == teamId)
                .all()
            )
            if not category_models:
                raise GetAllCategoriesByTeamIdNotFoundException(
                    "No categories found for the given team ID."
                )
            return [_to_domain(category_model) for category_model in category_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise CategoryRetrievalException("Failed to retrieve categories.")

    def UpdateCategoryById(
        self, categoryId: uuid.UUID, new_category: Category
    ) -> Category:
        try:
            category_model = (
                self.Db.query(CategoriesModel)
                .filter(CategoriesModel.id == categoryId)
                .first()
            )
            if not category_model:
                raise CategoryNotFoundException("Category not found.")

            category_model.name = new_category.name

            self.Db.commit()
            self.Db.refresh(category_model)
            return _to_domain(category_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise CategoryUpdateException("Failed to update category.")

    def DeleteCategoryById(self, categoryId: uuid.UUID) -> bool:
        try:
            category_model = (
                self.Db.query(CategoriesModel)
                .filter(CategoriesModel.id == categoryId)
                .first()
            )
            if not category_model:
                raise CategoryNotFoundException("Category not found.")

            self.Db.delete(category_model)
            self.Db.commit()
            return True

        except Exception as e:
            logging.error(f"Error: {e}")
            raise CategoryDeletionException("Failed to delete category.")
