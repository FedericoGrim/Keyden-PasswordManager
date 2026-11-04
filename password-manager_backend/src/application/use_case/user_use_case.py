import uuid

from application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserDTO, UserPublicDTO
from application.exceptions.user_use_Case_exceptions import *

from domain.interfaces.user_service_interface import IUserService
from domain.interfaces.team_service_interface import ITeamService
from domain.interfaces.team_perm_level_service_interface import ITeamPermLevelService
from domain.interfaces.team_member_service_interface import ITeamMembersService
from domain.interfaces.user_teams_keys_service_interface import IUserTeamKeyService
from domain.entities.team import Team
from domain.entities.team_perm_level import TeamPermLevel
from domain.entities.team_member import TeamMember
from domain.entities.user_teams_keys import UserTeamKey

PERSONAL_TEAM_NAME = "Me"
PERSONAL_TEAM_OWNER_PERM_LEVEL_NAME = "Owner"
PERSONAL_TEAM_OWNER_PERM_LEVEL_RANK = 0

class CreateUserUseCase:
    def __init__(
        self,
        UserRepository: IUserService,
        TeamRepository: ITeamService,
        TeamPermLevelRepository: ITeamPermLevelService,
        TeamMembersRepository: ITeamMembersService,
        UserTeamKeyRepository: IUserTeamKeyService,
    ):
        self.user_repository = UserRepository
        self.team_repository = TeamRepository
        self.team_perm_level_repository = TeamPermLevelRepository
        self.team_members_repository = TeamMembersRepository
        self.user_teams_keys_repository = UserTeamKeyRepository

    async def execute(self, user_create: CreateUserDTO) -> UserDTO:
        try:
            user_entity = user_create.to_entity()
            user = self.user_repository.create_user(user_entity)

            personal_team = self.team_repository.CreateTeam(
                Team(name=PERSONAL_TEAM_NAME, is_personal=True)
            )
            owner_perm_level = self.team_perm_level_repository.CreateTeamPermLevel(
                TeamPermLevel(
                    team_id=personal_team.id,
                    name=PERSONAL_TEAM_OWNER_PERM_LEVEL_NAME,
                    rank=PERSONAL_TEAM_OWNER_PERM_LEVEL_RANK,
                )
            )
            self.team_members_repository.add_member_to_team(
                TeamMember(
                    team_id=personal_team.id,
                    user_id=user.id,
                    perm_level_id=owner_perm_level.id,
                )
            )
            self.user_teams_keys_repository.add_key(
                UserTeamKey(
                    user_id=user.id,
                    team_id=personal_team.id,
                    team_key_encrypted=user_create.team_key_encrypted,
                )
            )

            return UserDTO.from_entity(user)

        except Exception as e:
            raise UserCreationException(str(e)) from e


class GetUserByKeycloakIdUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    def execute(self, main_user_id: uuid.UUID) -> UserDTO:
        try:
            user = self.user_repository.get_user_by_keycloak_id(main_user_id)
            return UserDTO.from_entity(user)

        except Exception as e:
            raise UserRetrievalException(str(e)) from e


class GetUserByUsernameAndCodeUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    def execute(self, username: str, code: str) -> UserPublicDTO:
        try:
            user = self.user_repository.get_user_by_username_and_code(username, code)
            return UserPublicDTO.from_entity(user)

        except Exception as e:
            raise UserRetrievalException(str(e)) from e


class GetUserByIdUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    def execute(self, user_id: uuid.UUID) -> UserPublicDTO:
        try:
            user = self.user_repository.get_user_by_id(user_id)
            return UserPublicDTO.from_entity(user)

        except Exception as e:
            raise UserRetrievalException(str(e)) from e


class UpdateUserByIdUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    async def execute(self, user_id: uuid.UUID, new_user: UpdateUserDTO) -> UserDTO:
        try:
            existing_user = self.user_repository.get_user_by_keycloak_id(user_id)
            new_user_entity = new_user.to_entity(existing_user=existing_user)
            updated = self.user_repository.update_user_by_id(user_id, new_user_entity)

            return UserDTO.from_entity(updated)

        except Exception as e:
            raise UserUpdateException(str(e)) from e


class DeleteUserByIdUseCase:
    def __init__(self, UserRepository: IUserService):
        self.user_repository = UserRepository

    async def execute(self, user_id: uuid.UUID):
        try:
            deleted = self.user_repository.delete_user_by_id(user_id)

            return deleted

        except Exception as e:
            raise UserDeletionException(str(e)) from e