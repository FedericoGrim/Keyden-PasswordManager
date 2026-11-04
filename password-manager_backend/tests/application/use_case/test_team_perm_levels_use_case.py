import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.team_perm_levels_dto import (
    CreateTeamPermLevelDTO,
    UpdateTeamPermLevelDTO,
)
from application.exceptions.team_perm_levels_use_case_exceptions import (
    CreateTeamPermLevelException,
    TeamPermLevelRetrievalException,
    TeamPermLevelUpdateException,
    TeamPermLevelDeletionException,
)
from application.use_case.team_perm_levels_use_case import (
    CreateTeamPermLevelUseCase,
    GetTeamPermLevelByIdUseCase,
    GetAllTeamPermLevelsByTeamIdUseCase,
    UpdateTeamPermLevelByIdUseCase,
    DeleteTeamPermLevelByIdUseCase,
)
from domain.entities.team_perm_level import TeamPermLevel
from domain.interfaces.team_perm_level_service_interface import ITeamPermLevelService


@pytest.fixture
def repo() -> MagicMock:
    return MagicMock(spec=ITeamPermLevelService)


class TestCreateTeamPermLevelUseCase:
    def test_creates_and_returns_repository_result(self, repo: MagicMock) -> None:
        team_id = uuid.uuid4()
        created = TeamPermLevel(id=uuid.uuid4(), team_id=team_id, name="Owner", rank=0)
        repo.CreateTeamPermLevel.return_value = created

        dto = CreateTeamPermLevelDTO(team_id=team_id, name="Owner", rank=0)
        result = CreateTeamPermLevelUseCase(repo).execute(dto, uuid.uuid4())

        assert result is created

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.CreateTeamPermLevel.side_effect = Exception("duplicate")
        dto = CreateTeamPermLevelDTO(team_id=uuid.uuid4(), name="Owner", rank=0)

        with pytest.raises(CreateTeamPermLevelException):
            CreateTeamPermLevelUseCase(repo).execute(dto, uuid.uuid4())


class TestGetTeamPermLevelByIdUseCase:
    def test_returns_dto(self, repo: MagicMock) -> None:
        perm_level = TeamPermLevel(
            id=uuid.uuid4(), team_id=uuid.uuid4(), name="Owner", rank=0
        )
        repo.GetTeamPermLevelById.return_value = perm_level

        assert perm_level.id is not None
        result = GetTeamPermLevelByIdUseCase(repo).execute(perm_level.id)

        assert result.name == "Owner"
        assert result.rank == 0

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.GetTeamPermLevelById.side_effect = Exception("not found")

        with pytest.raises(TeamPermLevelRetrievalException):
            GetTeamPermLevelByIdUseCase(repo).execute(uuid.uuid4())


class TestGetAllTeamPermLevelsByTeamIdUseCase:
    def test_maps_entities_to_dtos(self, repo: MagicMock) -> None:
        team_id = uuid.uuid4()
        perm_levels = [
            TeamPermLevel(id=uuid.uuid4(), team_id=team_id, name="Owner", rank=0),
            TeamPermLevel(id=uuid.uuid4(), team_id=team_id, name="Viewer", rank=1),
        ]
        repo.GetAllTeamPermLevelsByTeamId.return_value = perm_levels

        result = GetAllTeamPermLevelsByTeamIdUseCase(repo).execute(team_id)

        assert {dto.name for dto in result} == {"Owner", "Viewer"}

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.GetAllTeamPermLevelsByTeamId.side_effect = Exception("none")

        with pytest.raises(TeamPermLevelRetrievalException):
            GetAllTeamPermLevelsByTeamIdUseCase(repo).execute(uuid.uuid4())


class TestUpdateTeamPermLevelByIdUseCase:
    def test_looks_up_existing_then_updates(self, repo: MagicMock) -> None:
        perm_level_id = uuid.uuid4()
        existing = TeamPermLevel(
            id=perm_level_id, team_id=uuid.uuid4(), name="Owner", rank=0
        )
        updated = TeamPermLevel(
            id=perm_level_id, team_id=existing.team_id, name="Admin", rank=0
        )
        repo.GetTeamPermLevelById.return_value = existing
        repo.UpdateTeamPermLevelById.return_value = updated

        dto = UpdateTeamPermLevelDTO(name="Admin")
        result = UpdateTeamPermLevelByIdUseCase(repo).execute(
            perm_level_id, dto, uuid.uuid4()
        )

        assert result.name == "Admin"
        repo.GetTeamPermLevelById.assert_called_once_with(perm_level_id)

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.GetTeamPermLevelById.side_effect = Exception("missing")

        with pytest.raises(TeamPermLevelUpdateException):
            UpdateTeamPermLevelByIdUseCase(repo).execute(
                uuid.uuid4(), UpdateTeamPermLevelDTO(name="Admin"), uuid.uuid4()
            )


class TestDeleteTeamPermLevelByIdUseCase:
    def test_returns_repository_result(self, repo: MagicMock) -> None:
        repo.DeleteTeamPermLevelById.return_value = True

        result = DeleteTeamPermLevelByIdUseCase(repo).execute(
            uuid.uuid4(), uuid.uuid4()
        )

        assert result is True

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.DeleteTeamPermLevelById.side_effect = Exception("not found")

        with pytest.raises(TeamPermLevelDeletionException):
            DeleteTeamPermLevelByIdUseCase(repo).execute(uuid.uuid4(), uuid.uuid4())
