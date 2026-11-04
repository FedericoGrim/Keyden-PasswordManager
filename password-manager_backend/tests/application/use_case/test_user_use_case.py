from typing import Any
import uuid
from unittest.mock import MagicMock

import pytest

from application.dto.user_dto import CreateUserDTO, UpdateUserDTO
from application.exceptions.user_use_Case_exceptions import (
    UserCreationException,
    UserRetrievalException,
    UserUpdateException,
)
from application.use_case.user_use_case import (
    CreateUserUseCase,
    GetUserByKeycloakIdUseCase,
    GetUserByUsernameAndCodeUseCase,
    GetUserByIdUseCase,
    UpdateUserByIdUseCase,
    DeleteUserByIdUseCase,
    PERSONAL_TEAM_NAME,
    PERSONAL_TEAM_OWNER_PERM_LEVEL_NAME,
    PERSONAL_TEAM_OWNER_PERM_LEVEL_RANK,
)
from domain.entities.user import User
from domain.entities.team import Team
from domain.entities.team_perm_level import TeamPermLevel
from domain.interfaces.user_service_interface import IUserService
from domain.interfaces.team_service_interface import ITeamService
from domain.interfaces.team_perm_level_service_interface import ITeamPermLevelService
from domain.interfaces.team_member_service_interface import ITeamMembersService
from domain.interfaces.user_teams_keys_service_interface import IUserTeamKeyService


def make_user(**overrides: Any) -> User:  # noqa: ANN401
    defaults: dict[str, Any] = dict(
        id=uuid.uuid4(),
        keycloak_id=uuid.uuid4(),
        username="alice",
        code="ABC1234567",
        salt="salt",
        public_key_ec=b"pub_ec",
        private_key_ec=b"priv_ec",
        public_key_pq=b"pub_pq",
        private_key_pq=b"priv_pq",
    )
    defaults.update(overrides)
    return User(**defaults)


@pytest.fixture
def repos() -> dict[str, MagicMock]:
    return dict(
        user=MagicMock(spec=IUserService),
        team=MagicMock(spec=ITeamService),
        team_perm_level=MagicMock(spec=ITeamPermLevelService),
        team_members=MagicMock(spec=ITeamMembersService),
        user_teams_keys=MagicMock(spec=IUserTeamKeyService),
    )


class TestCreateUserUseCase:
    async def test_provisions_personal_team_and_owner_membership(
        self, repos: dict[str, MagicMock]
    ) -> None:
        user = make_user()
        team = Team(id=uuid.uuid4(), name=PERSONAL_TEAM_NAME, is_personal=True)
        assert team.id is not None
        perm_level = TeamPermLevel(
            id=uuid.uuid4(),
            team_id=team.id,
            name=PERSONAL_TEAM_OWNER_PERM_LEVEL_NAME,
            rank=PERSONAL_TEAM_OWNER_PERM_LEVEL_RANK,
        )

        repos["user"].create_user.return_value = user
        repos["team"].CreateTeam.return_value = team
        repos["team_perm_level"].CreateTeamPermLevel.return_value = perm_level

        use_case = CreateUserUseCase(
            UserRepository=repos["user"],
            TeamRepository=repos["team"],
            TeamPermLevelRepository=repos["team_perm_level"],
            TeamMembersRepository=repos["team_members"],
            UserTeamKeyRepository=repos["user_teams_keys"],
        )
        assert user.keycloak_id is not None
        assert user.id is not None
        dto = CreateUserDTO(
            id=user.id,
            keycloak_id=user.keycloak_id,
            username="alice",
            code="ABC1234567",
            salt="salt",
            public_key_ec=b"pub_ec",
            private_key_ec=b"priv_ec",
            public_key_pq=b"pub_pq",
            private_key_pq=b"priv_pq",
            team_key_encrypted="enc-team-key",
        )

        result = await use_case.execute(dto)

        assert result.id == user.id

        # A personal team is created for the new user...
        created_team = repos["team"].CreateTeam.call_args.args[0]
        assert created_team.is_personal is True

        # ...with an Owner permission level scoped to that team...
        created_perm_level = repos[
            "team_perm_level"
        ].CreateTeamPermLevel.call_args.args[0]
        assert created_perm_level.team_id == team.id
        assert created_perm_level.rank == PERSONAL_TEAM_OWNER_PERM_LEVEL_RANK

        # ...the user is added as a member with that Owner perm level...
        added_member = repos["team_members"].add_member_to_team.call_args.args[0]
        assert added_member.team_id == team.id
        assert added_member.user_id == user.id
        assert added_member.perm_level_id == perm_level.id

        # ...and the team key handed in the request is stored for that user/team pair.
        added_key = repos["user_teams_keys"].add_key.call_args.args[0]
        assert added_key.user_id == user.id
        assert added_key.team_id == team.id
        assert added_key.team_key_encrypted == "enc-team-key"

    async def test_wraps_errors_from_any_step(
        self, repos: dict[str, MagicMock]
    ) -> None:
        repos["user"].create_user.return_value = make_user()
        repos["team"].CreateTeam.side_effect = Exception("team creation failed")

        use_case = CreateUserUseCase(
            UserRepository=repos["user"],
            TeamRepository=repos["team"],
            TeamPermLevelRepository=repos["team_perm_level"],
            TeamMembersRepository=repos["team_members"],
            UserTeamKeyRepository=repos["user_teams_keys"],
        )
        dto = CreateUserDTO(
            id=uuid.uuid4(),
            keycloak_id=uuid.uuid4(),
            username="alice",
            code="ABC1234567",
            salt="salt",
            public_key_ec=b"a",
            private_key_ec=b"b",
            public_key_pq=b"c",
            private_key_pq=b"d",
            team_key_encrypted="enc-team-key",
        )

        with pytest.raises(UserCreationException):
            await use_case.execute(dto)


class TestGetUserByKeycloakIdUseCase:
    def test_returns_user_dto(self, repos: dict[str, MagicMock]) -> None:
        user = make_user()
        repos["user"].get_user_by_keycloak_id.return_value = user

        assert user.keycloak_id is not None
        result = GetUserByKeycloakIdUseCase(repos["user"]).execute(user.keycloak_id)

        assert result.id == user.id
        assert result.username == "alice"

    def test_wraps_repository_errors(self, repos: dict[str, MagicMock]) -> None:
        repos["user"].get_user_by_keycloak_id.side_effect = Exception("not found")

        with pytest.raises(UserRetrievalException):
            GetUserByKeycloakIdUseCase(repos["user"]).execute(uuid.uuid4())


class TestGetUserByUsernameAndCodeUseCase:
    def test_returns_public_dto_without_private_keys(
        self, repos: dict[str, MagicMock]
    ) -> None:
        user = make_user()
        repos["user"].get_user_by_username_and_code.return_value = user

        result = GetUserByUsernameAndCodeUseCase(repos["user"]).execute(
            "alice", "ABC1234567"
        )

        assert result.username == "alice"
        assert not hasattr(result, "private_key_ec")

    def test_wraps_repository_errors(self, repos: dict[str, MagicMock]) -> None:
        repos["user"].get_user_by_username_and_code.side_effect = Exception("not found")

        with pytest.raises(UserRetrievalException):
            GetUserByUsernameAndCodeUseCase(repos["user"]).execute(
                "alice", "ABC1234567"
            )


class TestGetUserByIdUseCase:
    def test_returns_public_dto(self, repos: dict[str, MagicMock]) -> None:
        user = make_user()
        repos["user"].get_user_by_id.return_value = user

        assert user.id is not None
        result = GetUserByIdUseCase(repos["user"]).execute(user.id)

        assert result.id == user.id

    def test_wraps_repository_errors(self, repos: dict[str, MagicMock]) -> None:
        repos["user"].get_user_by_id.side_effect = Exception("not found")

        with pytest.raises(UserRetrievalException):
            GetUserByIdUseCase(repos["user"]).execute(uuid.uuid4())


class TestUpdateUserByIdUseCase:
    async def test_merges_into_existing_and_returns_dto(
        self, repos: dict[str, MagicMock]
    ) -> None:
        existing = make_user(username="alice")
        updated = make_user(
            id=existing.id, keycloak_id=existing.keycloak_id, username="alice2"
        )
        repos["user"].get_user_by_keycloak_id.return_value = existing
        repos["user"].update_user_by_id.return_value = updated

        dto = UpdateUserDTO(
            keycloak_id=None,
            username="alice2",
            salt=None,
            public_key_ec=None,
            private_key_ec=None,
            public_key_pq=None,
            private_key_pq=None,
        )

        assert existing.keycloak_id is not None
        result = await UpdateUserByIdUseCase(repos["user"]).execute(
            existing.keycloak_id, dto
        )

        assert result.username == "alice2"

    async def test_wraps_repository_errors(self, repos: dict[str, MagicMock]) -> None:
        repos["user"].get_user_by_keycloak_id.side_effect = Exception("not found")
        dto = UpdateUserDTO(
            keycloak_id=None,
            username=None,
            salt=None,
            public_key_ec=None,
            private_key_ec=None,
            public_key_pq=None,
            private_key_pq=None,
        )

        with pytest.raises(UserUpdateException):
            await UpdateUserByIdUseCase(repos["user"]).execute(uuid.uuid4(), dto)


class TestDeleteUserByIdUseCase:
    async def test_returns_repository_result(self, repos: dict[str, MagicMock]) -> None:
        repos["user"].delete_user_by_id.return_value = {
            "message": "User deleted successfully."
        }

        result = await DeleteUserByIdUseCase(repos["user"]).execute(uuid.uuid4())

        assert result == {"message": "User deleted successfully."}
