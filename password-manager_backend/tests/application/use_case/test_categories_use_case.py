import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.categories_dto import CreateCategoryDTO, UpdateCategoryDTO
from application.exceptions.categories_use_case_exceptions import (
    CreateCategoryException,
    CategoryRetrievalException,
    CategoryUpdateException,
    CategoryDeletionException,
)
from application.use_case.categories_use_case import (
    CreateCategoriesUseCase,
    GetAllCategoriesByTeamIdUseCase,
    UpdateCategoryByIdUseCase,
    DeleteCategoryByIdUseCase,
)
from domain.entities.categories import Category
from domain.interfaces.icategories import ICategoriesService


@pytest.fixture
def repo() -> MagicMock:
    return MagicMock(spec=ICategoriesService)


class TestCreateCategoriesUseCase:
    def test_creates_and_returns_repository_result(self, repo: MagicMock):
        team_id = uuid.uuid4()
        created = Category(id=uuid.uuid4(), team_id=team_id, name="Work")
        repo.CreateCategory.return_value = created

        result = CreateCategoriesUseCase(repo).execute(CreateCategoryDTO(team_id=team_id, name="Work"), uuid.uuid4())

        assert result is created

    def test_wraps_repository_errors(self, repo: MagicMock):
        repo.CreateCategory.side_effect = Exception("duplicate")

        with pytest.raises(CreateCategoryException):
            CreateCategoriesUseCase(repo).execute(CreateCategoryDTO(team_id=uuid.uuid4(), name="Work"), uuid.uuid4())


class TestGetAllCategoriesByTeamIdUseCase:
    def test_maps_entities_to_dtos(self, repo: MagicMock):
        team_id = uuid.uuid4()
        categories = [Category(id=uuid.uuid4(), team_id=team_id, name="Work"), Category(id=uuid.uuid4(), team_id=team_id, name="Personal")]
        repo.GetAllCategoriesByTeamId.return_value = categories

        result = GetAllCategoriesByTeamIdUseCase(repo).execute(team_id)

        assert {dto.name for dto in result} == {"Work", "Personal"}

    def test_wraps_repository_errors(self, repo: MagicMock):
        repo.GetAllCategoriesByTeamId.side_effect = Exception("none")

        with pytest.raises(CategoryRetrievalException):
            GetAllCategoriesByTeamIdUseCase(repo).execute(uuid.uuid4())


class TestUpdateCategoryByIdUseCase:
    def test_returns_updated_dto(self, repo: MagicMock):
        category_id = uuid.uuid4()
        updated = Category(id=category_id, team_id=uuid.uuid4(), name="Renamed")
        repo.UpdateCategoryById.return_value = updated

        result = UpdateCategoryByIdUseCase(repo).execute(category_id, UpdateCategoryDTO(name="Renamed"), uuid.uuid4())

        assert result.name == "Renamed"
        repo.UpdateCategoryById.assert_called_once()
        assert repo.UpdateCategoryById.call_args.args[0] == category_id

    def test_wraps_repository_errors(self, repo: MagicMock):
        repo.UpdateCategoryById.side_effect = Exception("not found")

        with pytest.raises(CategoryUpdateException):
            UpdateCategoryByIdUseCase(repo).execute(uuid.uuid4(), UpdateCategoryDTO(name="X"), uuid.uuid4())


class TestDeleteCategoryByIdUseCase:
    def test_returns_repository_result(self, repo: MagicMock):
        repo.DeleteCategoryById.return_value = True

        result = DeleteCategoryByIdUseCase(repo).execute(uuid.uuid4(), uuid.uuid4())

        assert result is True

    def test_wraps_repository_errors(self, repo: MagicMock):
        repo.DeleteCategoryById.side_effect = Exception("not found")

        with pytest.raises(CategoryDeletionException):
            DeleteCategoryByIdUseCase(repo).execute(uuid.uuid4(), uuid.uuid4())
