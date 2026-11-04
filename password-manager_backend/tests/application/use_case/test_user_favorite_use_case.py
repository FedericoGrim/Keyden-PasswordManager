import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.user_favorite_dto import CreateFavoriteDTO
from application.exceptions.user_favorite_use_case_exceptions import (
    UserFavoriteAdditionException,
    UserFavoriteRetrievalException,
    UserFavoriteRemovalException,
)
from application.use_case.user_favorite_use_case import (
    AddFavoriteUseCase,
    GetFavoritesByUserIdUseCase,
    RemoveFavoriteUseCase,
)
from domain.entities.user_favorite import UserFavorite
from domain.interfaces.user_favorite_service_interface import IUserFavoriteService


@pytest.fixture
def repo():
    return MagicMock(spec=IUserFavoriteService)


class TestAddFavoriteUseCase:
    def test_returns_dto_from_repository_result(self, repo):
        favorite = UserFavorite(
            id=uuid.uuid4(), user_id=uuid.uuid4(), sub_account_id=uuid.uuid4()
        )
        repo.add_favorite.return_value = favorite

        dto = CreateFavoriteDTO(
            user_id=favorite.user_id, sub_account_id=favorite.sub_account_id
        )
        result = AddFavoriteUseCase(repo).execute(dto)

        assert result.id == favorite.id
        assert result.user_id == favorite.user_id

    def test_wraps_repository_errors(self, repo):
        repo.add_favorite.side_effect = Exception("already a favorite")
        dto = CreateFavoriteDTO(user_id=uuid.uuid4(), sub_account_id=uuid.uuid4())

        with pytest.raises(UserFavoriteAdditionException):
            AddFavoriteUseCase(repo).execute(dto)


class TestGetFavoritesByUserIdUseCase:
    def test_maps_entities_to_dtos(self, repo):
        user_id = uuid.uuid4()
        favorites = [
            UserFavorite(id=uuid.uuid4(), user_id=user_id, sub_account_id=uuid.uuid4()),
            UserFavorite(id=uuid.uuid4(), user_id=user_id, sub_account_id=uuid.uuid4()),
        ]
        repo.get_favorites_by_user_id.return_value = favorites

        result = GetFavoritesByUserIdUseCase(repo).execute(user_id)

        assert len(result) == 2
        assert all(dto.user_id == user_id for dto in result)

    def test_wraps_repository_errors(self, repo):
        repo.get_favorites_by_user_id.side_effect = Exception("boom")

        with pytest.raises(UserFavoriteRetrievalException):
            GetFavoritesByUserIdUseCase(repo).execute(uuid.uuid4())


class TestRemoveFavoriteUseCase:
    def test_returns_repository_result(self, repo):
        repo.remove_favorite.return_value = {
            "message": "Favorite removed successfully."
        }
        user_id, sub_account_id = uuid.uuid4(), uuid.uuid4()

        result = RemoveFavoriteUseCase(repo).execute(user_id, sub_account_id)

        assert result == {"message": "Favorite removed successfully."}
        repo.remove_favorite.assert_called_once_with(user_id, sub_account_id)

    def test_wraps_repository_errors(self, repo):
        repo.remove_favorite.side_effect = Exception("not found")

        with pytest.raises(UserFavoriteRemovalException):
            RemoveFavoriteUseCase(repo).execute(uuid.uuid4(), uuid.uuid4())
