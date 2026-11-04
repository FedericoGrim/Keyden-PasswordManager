import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.team_dto import CreateTeamDTO, UpdateTeamDTO, DeleteTeamDTO
from application.exceptions.team_use_case_exceptions import (
    TeamCreationException,
    TeamRetrievalByIdException,
    TeamsRetrievalByUserIdException,
    TeamUpdateException,
    TeamDeleteException,
)
from application.use_case.team_use_case import (
    CreateTeamUseCase,
    GetTeamByIdUseCase,
    GetTeamsByUserIdUseCase,
    UpdateTeamByIdUseCase,
    DeleteTeamByIdUseCase,
)
from domain.entities.team import Team
from domain.interfaces.team_service_interface import ITeamService


@pytest.fixture
def repo():
    return MagicMock(spec=ITeamService)


class TestCreateTeamUseCase:
    def test_creates_and_returns_repository_result(self, repo):
        created = Team(id=uuid.uuid4(), name="Engineering", is_personal=False)
        repo.CreateTeam.return_value = created

        result = CreateTeamUseCase(repo).execute(
            uuid.uuid4(), CreateTeamDTO(name="Engineering")
        )

        assert result is created
        passed_entity = repo.CreateTeam.call_args.args[0]
        assert passed_entity.name == "Engineering"
        assert passed_entity.is_personal is False

    def test_wraps_repository_errors(self, repo):
        repo.CreateTeam.side_effect = Exception("duplicate")

        with pytest.raises(TeamCreationException):
            CreateTeamUseCase(repo).execute(
                uuid.uuid4(), CreateTeamDTO(name="Engineering")
            )


class TestGetTeamByIdUseCase:
    def test_returns_team_dto(self, repo):
        team = Team(id=uuid.uuid4(), name="Engineering", is_personal=False)
        repo.GetTeamById.return_value = team

        result = GetTeamByIdUseCase(repo).execute(team.id)

        assert result.id == team.id
        assert result.name == "Engineering"
        assert result.is_personal is False

    def test_wraps_repository_errors(self, repo):
        repo.GetTeamById.side_effect = Exception("not found")

        with pytest.raises(TeamRetrievalByIdException):
            GetTeamByIdUseCase(repo).execute(uuid.uuid4())


class TestGetTeamsByUserIdUseCase:
    def test_maps_entities_to_dtos(self, repo):
        teams = [
            Team(id=uuid.uuid4(), name="Me", is_personal=True),
            Team(id=uuid.uuid4(), name="Work", is_personal=False),
        ]
        repo.GetTeamsByUserId.return_value = teams

        result = GetTeamsByUserIdUseCase(repo).execute(uuid.uuid4())

        assert len(result) == 2
        assert {dto.name for dto in result} == {"Me", "Work"}

    def test_wraps_repository_errors(self, repo):
        repo.GetTeamsByUserId.side_effect = Exception("none found")

        with pytest.raises(TeamsRetrievalByUserIdException):
            GetTeamsByUserIdUseCase(repo).execute(uuid.uuid4())


class TestUpdateTeamByIdUseCase:
    def test_merges_into_existing_and_returns_dto(self, repo):
        existing = Team(id=uuid.uuid4(), name="Old Name", is_personal=False)
        updated = Team(id=existing.id, name="New Name", is_personal=False)
        repo.GetTeamById.return_value = existing
        repo.UpdateTeamById.return_value = updated

        dto = UpdateTeamDTO(id=existing.id, name="New Name")

        result = UpdateTeamByIdUseCase(repo).execute(uuid.uuid4(), dto)

        assert result.name == "New Name"
        repo.GetTeamById.assert_called_once_with(existing.id)

    def test_wraps_repository_errors(self, repo):
        repo.GetTeamById.side_effect = Exception("missing")

        with pytest.raises(TeamUpdateException):
            UpdateTeamByIdUseCase(repo).execute(
                uuid.uuid4(), UpdateTeamDTO(id=uuid.uuid4(), name="X")
            )


class TestDeleteTeamByIdUseCase:
    def test_calls_repository_delete(self, repo):
        team_id = uuid.uuid4()

        DeleteTeamByIdUseCase(repo).execute(uuid.uuid4(), DeleteTeamDTO(id=team_id))

        repo.DeleteTeamById.assert_called_once_with(team_id)

    def test_wraps_repository_errors(self, repo):
        repo.DeleteTeamById.side_effect = Exception("cannot delete")

        with pytest.raises(TeamDeleteException):
            DeleteTeamByIdUseCase(repo).execute(
                uuid.uuid4(), DeleteTeamDTO(id=uuid.uuid4())
            )
