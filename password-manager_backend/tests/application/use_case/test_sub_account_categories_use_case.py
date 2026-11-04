import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.sub_account_categories_dto import (
    CreateSubAccountCategoryDTO,
    SubAccountCategoriesDTO,
)
from application.exceptions.sub_account_categories_use_case_exceptions import (
    CreateSubAccountCategoryException,
    SubAccountCategoryRetrievalException,
    SubAccountCategoryDeletionException,
)
from application.use_case.sub_account_categories_use_case import (
    CreateSubAccountCategoryUseCase,
    GetAllCategoriesBySubAccountIdUseCase,
    DeleteSubAccountCategoryUseCase,
)
from domain.entities.sub_account_categories import SubAccountCategories
from domain.interfaces.isub_account_categories_service import (
    ISubAccountCategoriesService,
)


@pytest.fixture
def repo() -> MagicMock:
    return MagicMock(spec=ISubAccountCategoriesService)


class TestCreateSubAccountCategoryUseCase:
    def test_creates_and_returns_repository_result(self, repo: MagicMock):
        created = SubAccountCategories(
            id=uuid.uuid4(), sub_account_id=uuid.uuid4(), category_id=uuid.uuid4()
        )
        repo.CreateSubAccountCategory.return_value = created

        dto = CreateSubAccountCategoryDTO(
            sub_account_id=created.sub_account_id, category_id=created.category_id
        )
        result = CreateSubAccountCategoryUseCase(repo).execute(dto)

        assert result is created

    def test_wraps_repository_errors(self, repo: MagicMock):
        repo.CreateSubAccountCategory.side_effect = Exception("duplicate")
        dto = CreateSubAccountCategoryDTO(
            sub_account_id=uuid.uuid4(), category_id=uuid.uuid4()
        )

        with pytest.raises(CreateSubAccountCategoryException):
            CreateSubAccountCategoryUseCase(repo).execute(dto)


class TestGetAllCategoriesBySubAccountIdUseCase:
    def test_maps_entities_to_dtos(self, repo: MagicMock):
        sub_account_id = uuid.uuid4()
        entities = [
            SubAccountCategories(
                id=uuid.uuid4(), sub_account_id=sub_account_id, category_id=uuid.uuid4()
            ),
            SubAccountCategories(
                id=uuid.uuid4(), sub_account_id=sub_account_id, category_id=uuid.uuid4()
            ),
        ]
        repo.GetAllCategoriesBySubAccountId.return_value = entities

        result = GetAllCategoriesBySubAccountIdUseCase(repo).execute(sub_account_id)

        assert len(result) == 2
        assert all(dto.sub_account_id == sub_account_id for dto in result)

    def test_wraps_repository_errors(self, repo: MagicMock):
        repo.GetAllCategoriesBySubAccountId.side_effect = Exception("none")

        with pytest.raises(SubAccountCategoryRetrievalException):
            GetAllCategoriesBySubAccountIdUseCase(repo).execute(uuid.uuid4())


class TestDeleteSubAccountCategoryUseCase:
    def test_returns_repository_result(self, repo: MagicMock):
        repo.DeleteSubAccountCategory.return_value = True
        dto = SubAccountCategoriesDTO(
            sub_account_id=uuid.uuid4(), category_id=uuid.uuid4()
        )

        result = DeleteSubAccountCategoryUseCase(repo).execute(dto)

        assert result is True

    def test_wraps_repository_errors(self, repo: MagicMock):
        repo.DeleteSubAccountCategory.side_effect = Exception("not found")
        dto = SubAccountCategoriesDTO(
            sub_account_id=uuid.uuid4(), category_id=uuid.uuid4()
        )

        with pytest.raises(SubAccountCategoryDeletionException):
            DeleteSubAccountCategoryUseCase(repo).execute(dto)
