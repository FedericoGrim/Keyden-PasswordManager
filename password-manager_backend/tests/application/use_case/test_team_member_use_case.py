from typing import Any
import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.team_member_dto import (
    CreateTeamMemberDTO,
    UpdateTeamMemberDTO,
    RemoveTeamMemberDTO,
)
from application.exceptions.team_member_use_case_exceptions import (
    TeamMemberAdditionException,
    TeamMemberRetrievalByIdException,
    TeamMembersRetrievalByTeamIdException,
    TeamMemberRoleUpdateException,
    TeamMemberRemovalException,
)
from application.use_case.team_member_use_case import (
    AddMemberToTeamUseCase,
    GetTeamMemberByIdUseCase,
    GetTeamMembersByTeamIdUseCase,
    UpdateTeamMemberRoleUseCase,
    RemoveMemberFromTeamUseCase,
)
from domain.entities.team_member import TeamMember
from domain.interfaces.team_member_service_interface import ITeamMembersService


@pytest.fixture
def repo() -> MagicMock:
    return MagicMock(spec=ITeamMembersService)


def make_member(**overrides: Any) -> TeamMember:  # noqa: ANN401
    defaults: dict[str, Any] = dict(
        id=uuid.uuid4(),
        team_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        perm_level_id=uuid.uuid4(),
    )
    defaults.update(overrides)
    return TeamMember(**defaults)


class TestAddMemberToTeamUseCase:
    def test_returns_dto_from_repository_result(self, repo: MagicMock) -> None:
        member = make_member()
        repo.add_member_to_team.return_value = member

        dto = CreateTeamMemberDTO(
            user_id=member.user_id,
            team_id=member.team_id,
            perm_level_id=member.perm_level_id,
        )
        result = AddMemberToTeamUseCase(repo).execute(uuid.uuid4(), dto)

        assert result.id == member.id
        assert result.user_id == member.user_id

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.add_member_to_team.side_effect = Exception("already a member")
        dto = CreateTeamMemberDTO(
            user_id=uuid.uuid4(), team_id=uuid.uuid4(), perm_level_id=uuid.uuid4()
        )

        with pytest.raises(TeamMemberAdditionException):
            AddMemberToTeamUseCase(repo).execute(uuid.uuid4(), dto)


class TestGetTeamMemberByIdUseCase:
    def test_returns_dto(self, repo: MagicMock) -> None:
        member = make_member()
        repo.get_team_member_by_id.return_value = member

        assert member.id is not None
        result = GetTeamMemberByIdUseCase(repo).execute(member.id)

        assert result.id == member.id

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.get_team_member_by_id.side_effect = Exception("not found")

        with pytest.raises(TeamMemberRetrievalByIdException):
            GetTeamMemberByIdUseCase(repo).execute(uuid.uuid4())


class TestGetTeamMembersByTeamIdUseCase:
    def test_maps_entities_to_dtos(self, repo: MagicMock) -> None:
        team_id = uuid.uuid4()
        members = [make_member(team_id=team_id), make_member(team_id=team_id)]
        repo.get_members_by_team_id.return_value = members

        result = GetTeamMembersByTeamIdUseCase(repo).execute(team_id)

        assert len(result) == 2

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.get_members_by_team_id.side_effect = Exception("boom")

        with pytest.raises(TeamMembersRetrievalByTeamIdException):
            GetTeamMembersByTeamIdUseCase(repo).execute(uuid.uuid4())


class TestUpdateTeamMemberRoleUseCase:
    def test_looks_up_existing_member_then_updates(self, repo: MagicMock) -> None:
        existing = make_member()
        new_perm_level_id = uuid.uuid4()
        updated = make_member(
            id=existing.id,
            team_id=existing.team_id,
            user_id=existing.user_id,
            perm_level_id=new_perm_level_id,
        )
        repo.get_team_member_by_user_and_team.return_value = existing
        repo.update_member_role.return_value = updated

        dto = UpdateTeamMemberDTO(
            user_id=existing.user_id,
            team_id=existing.team_id,
            perm_level_id=new_perm_level_id,
        )
        result = UpdateTeamMemberRoleUseCase(repo).execute(uuid.uuid4(), dto)

        assert result.perm_level_id == new_perm_level_id
        repo.get_team_member_by_user_and_team.assert_called_once_with(
            existing.user_id, existing.team_id
        )

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.get_team_member_by_user_and_team.side_effect = Exception("missing")
        dto = UpdateTeamMemberDTO(
            user_id=uuid.uuid4(), team_id=uuid.uuid4(), perm_level_id=uuid.uuid4()
        )

        with pytest.raises(TeamMemberRoleUpdateException):
            UpdateTeamMemberRoleUseCase(repo).execute(uuid.uuid4(), dto)


class TestRemoveMemberFromTeamUseCase:
    def test_returns_repository_result(self, repo: MagicMock) -> None:
        repo.remove_member_from_team.return_value = {
            "message": "Member removed from team successfully."
        }
        member_id, team_id = uuid.uuid4(), uuid.uuid4()

        result = RemoveMemberFromTeamUseCase(repo).execute(
            uuid.uuid4(), RemoveTeamMemberDTO(member_id=member_id, team_id=team_id)
        )

        assert result == {"message": "Member removed from team successfully."}
        repo.remove_member_from_team.assert_called_once_with(
            member_id=member_id, team_id=team_id
        )

    def test_wraps_repository_errors(self, repo: MagicMock) -> None:
        repo.remove_member_from_team.side_effect = Exception("not in team")

        with pytest.raises(TeamMemberRemovalException):
            RemoveMemberFromTeamUseCase(repo).execute(
                uuid.uuid4(),
                RemoveTeamMemberDTO(member_id=uuid.uuid4(), team_id=uuid.uuid4()),
            )
