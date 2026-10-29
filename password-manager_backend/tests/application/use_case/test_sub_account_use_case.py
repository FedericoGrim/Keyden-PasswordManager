import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.sub_account_dto import CreateSubAccountDTO, UpdateSubAccountDTO, DeleteSubAccountDTO
from application.exceptions.sub_account_use_case_exceptions import (
    CreateSubAccountException,
    SubAccountRetrievalException,
    SubAccountUpdateException,
    SubAccountDeletionException,
)
from application.use_case.sub_account_use_case import (
    CreateSubAccountUseCase,
    GetSubAccountByIdUseCase,
    GetAllSubAccountsByTeamIdUseCase,
    UpdateSubAccountByIdUseCase,
    DeleteSubAccountByIdUseCase,
)
from domain.entities.sub_account import SubAccount
from domain.interfaces.sub_account_service_interface import ISubAccountService
from domain.interfaces.sub_account_history_service_interface import ISubAccountHistoryService


@pytest.fixture
def repo():
    return MagicMock(spec=ISubAccountService)


@pytest.fixture
def history_repo():
    return MagicMock(spec=ISubAccountHistoryService)


def make_sub_account(**overrides):
    defaults = dict(
        id=uuid.uuid4(),
        team_id=uuid.uuid4(),
        password_encrypted="enc-pass",
        required_perm_level_id=uuid.uuid4(),
        username_encrypted="enc-user",
        email_encrypted="enc-email",
        site_link_encrypted="enc-link",
        dek_wrapped="enc-dek",
    )
    defaults.update(overrides)
    return SubAccount(**defaults)


class TestCreateSubAccountUseCase:
    def test_creates_and_returns_repository_result(self, repo):
        created = make_sub_account()
        repo.CreateSubAccount.return_value = created

        dto = CreateSubAccountDTO(
            team_id=created.team_id,
            username_encrypted="enc-user",
            email_encrypted="enc-email",
            password_encrypted="enc-pass",
            site_link_encrypted="enc-link",
            required_perm_level_id=created.required_perm_level_id,
            dek_wrapped="enc-dek",
        )

        result = CreateSubAccountUseCase(repo).execute(uuid.uuid4(), dto)

        assert result is created
        repo.CreateSubAccount.assert_called_once()
        passed_entity = repo.CreateSubAccount.call_args.args[0]
        assert isinstance(passed_entity, SubAccount)
        assert passed_entity.team_id == created.team_id

    def test_wraps_repository_errors(self, repo):
        repo.CreateSubAccount.side_effect = Exception("db exploded")
        dto = CreateSubAccountDTO(
            team_id=uuid.uuid4(),
            username_encrypted="u",
            email_encrypted="e",
            password_encrypted="p",
            site_link_encrypted="s",
            required_perm_level_id=uuid.uuid4(),
            dek_wrapped="d",
        )

        with pytest.raises(CreateSubAccountException) as exc_info:
            CreateSubAccountUseCase(repo).execute(uuid.uuid4(), dto)

        assert "db exploded" in str(exc_info.value)


class TestGetSubAccountByIdUseCase:
    def test_returns_repository_result(self, repo):
        found = make_sub_account()
        repo.GetSubAccountById.return_value = found

        result = GetSubAccountByIdUseCase(repo).execute(found.id)

        assert result is found
        repo.GetSubAccountById.assert_called_once_with(found.id)

    def test_wraps_not_found_error(self, repo):
        repo.GetSubAccountById.side_effect = Exception("not found")

        with pytest.raises(SubAccountRetrievalException):
            GetSubAccountByIdUseCase(repo).execute(uuid.uuid4())


class TestGetAllSubAccountsByTeamIdUseCase:
    def test_maps_entities_to_dtos(self, repo):
        team_id = uuid.uuid4()
        entities = [make_sub_account(team_id=team_id), make_sub_account(team_id=team_id)]
        repo.GetAllSubAccountsByTeamId.return_value = entities

        result = GetAllSubAccountsByTeamIdUseCase(repo).execute(team_id)

        assert len(result) == 2
        assert {dto.id for dto in result} == {e.id for e in entities}
        assert all(dto.team_id == team_id for dto in result)

    def test_wraps_repository_errors(self, repo):
        repo.GetAllSubAccountsByTeamId.side_effect = Exception("boom")

        with pytest.raises(SubAccountRetrievalException):
            GetAllSubAccountsByTeamIdUseCase(repo).execute(uuid.uuid4())


class TestUpdateSubAccountByIdUseCase:
    def test_merges_into_existing_and_returns_dto(self, repo, history_repo):
        existing = make_sub_account(username_encrypted="old-user")
        updated = make_sub_account(id=existing.id, team_id=existing.team_id, username_encrypted="new-user")
        repo.GetSubAccountById.return_value = existing
        repo.UpdateSubAccountById.return_value = updated

        dto = UpdateSubAccountDTO(
            id=existing.id,
            username_encrypted="new-user",
            email_encrypted=None,
            password_encrypted=None,
            site_link_encrypted=None,
            required_perm_level_id=None,
        )

        result = UpdateSubAccountByIdUseCase(repo, history_repo).execute(uuid.uuid4(), dto)

        assert result.id == existing.id
        assert result.username_encrypted == "new-user"
        repo.GetSubAccountById.assert_called_once_with(existing.id)
        history_repo.CreateHistoryEntry.assert_called_once()

    def test_wraps_repository_errors(self, repo, history_repo):
        repo.GetSubAccountById.side_effect = Exception("missing")
        dto = UpdateSubAccountDTO(
            id=uuid.uuid4(),
            username_encrypted=None,
            email_encrypted=None,
            password_encrypted=None,
            site_link_encrypted=None,
            required_perm_level_id=None,
        )

        with pytest.raises(SubAccountUpdateException):
            UpdateSubAccountByIdUseCase(repo, history_repo).execute(uuid.uuid4(), dto)


class TestDeleteSubAccountByIdUseCase:
    def test_returns_repository_result(self, repo):
        repo.DeleteSubAccountById.return_value = {"message": "SubAccount deleted successfully."}
        sub_account_id = uuid.uuid4()

        result = DeleteSubAccountByIdUseCase(repo).execute(uuid.uuid4(), DeleteSubAccountDTO(id=sub_account_id))

        assert result == {"message": "SubAccount deleted successfully."}
        repo.DeleteSubAccountById.assert_called_once_with(sub_account_id)

    def test_wraps_repository_errors(self, repo):
        repo.DeleteSubAccountById.side_effect = Exception("cannot delete")

        with pytest.raises(SubAccountDeletionException):
            DeleteSubAccountByIdUseCase(repo).execute(uuid.uuid4(), DeleteSubAccountDTO(id=uuid.uuid4()))
