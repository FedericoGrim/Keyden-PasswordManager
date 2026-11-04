import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.user_teams_keys_dto import (
    CreateUserTeamKeyDTO,
    UpdateUserTeamKeyDTO,
    RemoveUserTeamKeyDTO,
)
from application.exceptions.user_teams_keys_use_case_exceptions import (
    UserTeamKeyAdditionException,
    UserTeamKeyRetrievalByIdException,
    UserTeamKeysRetrievalByTeamIdException,
    UserTeamKeysRetrievalByUserIdException,
    UserTeamKeyUpdateException,
    UserTeamKeyRemovalException,
)
from application.use_case.user_teams_keys_use_case import (
    AddUserTeamKeyUseCase,
    GetUserTeamKeyByIdUseCase,
    GetUserTeamKeysByTeamIdUseCase,
    GetUserTeamKeysByUserIdUseCase,
    UpdateUserTeamKeyUseCase,
    RemoveUserTeamKeyUseCase,
)
from domain.entities.user_teams_keys import UserTeamKey
from domain.interfaces.user_teams_keys_service_interface import IUserTeamKeyService


@pytest.fixture
def repo():
    return MagicMock(spec=IUserTeamKeyService)


def make_key(**overrides):
    defaults = dict(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        team_id=uuid.uuid4(),
        team_key_encrypted="enc-key",
    )
    defaults.update(overrides)
    return UserTeamKey(**defaults)


class TestAddUserTeamKeyUseCase:
    def test_returns_dto_from_repository_result(self, repo):
        key = make_key()
        repo.add_key.return_value = key

        dto = CreateUserTeamKeyDTO(
            user_id=key.user_id, team_id=key.team_id, team_key_encrypted="enc-key"
        )
        result = AddUserTeamKeyUseCase(repo).execute(uuid.uuid4(), dto)

        assert result.id == key.id

    def test_wraps_repository_errors(self, repo):
        repo.add_key.side_effect = Exception("already exists")
        dto = CreateUserTeamKeyDTO(
            user_id=uuid.uuid4(), team_id=uuid.uuid4(), team_key_encrypted="k"
        )

        with pytest.raises(UserTeamKeyAdditionException):
            AddUserTeamKeyUseCase(repo).execute(uuid.uuid4(), dto)


class TestGetUserTeamKeyByIdUseCase:
    def test_returns_dto(self, repo):
        key = make_key()
        repo.get_key_by_id.return_value = key

        result = GetUserTeamKeyByIdUseCase(repo).execute(key.id)

        assert result.team_key_encrypted == "enc-key"

    def test_wraps_repository_errors(self, repo):
        repo.get_key_by_id.side_effect = Exception("not found")

        with pytest.raises(UserTeamKeyRetrievalByIdException):
            GetUserTeamKeyByIdUseCase(repo).execute(uuid.uuid4())


class TestGetUserTeamKeysByTeamIdUseCase:
    def test_maps_entities_to_dtos(self, repo):
        team_id = uuid.uuid4()
        keys = [make_key(team_id=team_id), make_key(team_id=team_id)]
        repo.get_keys_by_team_id.return_value = keys

        result = GetUserTeamKeysByTeamIdUseCase(repo).execute(team_id)

        assert len(result) == 2

    def test_wraps_repository_errors(self, repo):
        repo.get_keys_by_team_id.side_effect = Exception("boom")

        with pytest.raises(UserTeamKeysRetrievalByTeamIdException):
            GetUserTeamKeysByTeamIdUseCase(repo).execute(uuid.uuid4())


class TestGetUserTeamKeysByUserIdUseCase:
    def test_maps_entities_to_dtos(self, repo):
        user_id = uuid.uuid4()
        keys = [make_key(user_id=user_id)]
        repo.get_keys_by_user_id.return_value = keys

        result = GetUserTeamKeysByUserIdUseCase(repo).execute(user_id)

        assert len(result) == 1

    def test_wraps_repository_errors(self, repo):
        repo.get_keys_by_user_id.side_effect = Exception("boom")

        with pytest.raises(UserTeamKeysRetrievalByUserIdException):
            GetUserTeamKeysByUserIdUseCase(repo).execute(uuid.uuid4())


class TestUpdateUserTeamKeyUseCase:
    def test_finds_matching_team_key_then_updates(self, repo):
        user_id, team_id = uuid.uuid4(), uuid.uuid4()
        existing = make_key(
            user_id=user_id, team_id=team_id, team_key_encrypted="old-key"
        )
        other_team_key = make_key(
            user_id=user_id, team_id=uuid.uuid4(), team_key_encrypted="other-key"
        )
        updated = make_key(
            id=existing.id,
            user_id=user_id,
            team_id=team_id,
            team_key_encrypted="new-key",
        )
        repo.get_keys_by_user_id.return_value = [other_team_key, existing]
        repo.update_key.return_value = updated

        dto = UpdateUserTeamKeyDTO(
            user_id=user_id, team_id=team_id, team_key_encrypted="new-key"
        )
        result = UpdateUserTeamKeyUseCase(repo).execute(uuid.uuid4(), dto)

        assert result.team_key_encrypted == "new-key"

    def test_raises_when_no_key_for_team(self, repo):
        user_id, team_id = uuid.uuid4(), uuid.uuid4()
        repo.get_keys_by_user_id.return_value = []

        dto = UpdateUserTeamKeyDTO(
            user_id=user_id, team_id=team_id, team_key_encrypted="new-key"
        )

        with pytest.raises(UserTeamKeyUpdateException) as exc_info:
            UpdateUserTeamKeyUseCase(repo).execute(uuid.uuid4(), dto)

        assert "not found" in str(exc_info.value).lower()

    def test_wraps_repository_errors(self, repo):
        repo.get_keys_by_user_id.side_effect = Exception("db error")
        dto = UpdateUserTeamKeyDTO(
            user_id=uuid.uuid4(), team_id=uuid.uuid4(), team_key_encrypted="k"
        )

        with pytest.raises(UserTeamKeyUpdateException):
            UpdateUserTeamKeyUseCase(repo).execute(uuid.uuid4(), dto)


class TestRemoveUserTeamKeyUseCase:
    def test_returns_repository_result(self, repo):
        repo.remove_key.return_value = {"message": "Key removed successfully."}
        user_id, team_id = uuid.uuid4(), uuid.uuid4()

        result = RemoveUserTeamKeyUseCase(repo).execute(
            uuid.uuid4(), RemoveUserTeamKeyDTO(user_id=user_id, team_id=team_id)
        )

        assert result == {"message": "Key removed successfully."}
        repo.remove_key.assert_called_once_with(user_id=user_id, team_id=team_id)

    def test_wraps_repository_errors(self, repo):
        repo.remove_key.side_effect = Exception("not found")

        with pytest.raises(UserTeamKeyRemovalException):
            RemoveUserTeamKeyUseCase(repo).execute(
                uuid.uuid4(),
                RemoveUserTeamKeyDTO(user_id=uuid.uuid4(), team_id=uuid.uuid4()),
            )
