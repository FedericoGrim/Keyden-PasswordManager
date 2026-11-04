import uuid

from application.exceptions.user_teams_keys_use_case_exceptions import *
from application.dto.user_teams_keys_dto import (
    UserTeamKeyDTO,
    CreateUserTeamKeyDTO,
    UpdateUserTeamKeyDTO,
    RemoveUserTeamKeyDTO,
)

from domain.interfaces.user_teams_keys_service_interface import IUserTeamKeyService


class AddUserTeamKeyUseCase:
    def __init__(self, UserTeamKeyRepository: IUserTeamKeyService):
        self.user_teams_keys_repository = UserTeamKeyRepository

    def execute(
        self, interactor_id: uuid.UUID, new_key: CreateUserTeamKeyDTO
    ) -> UserTeamKeyDTO:
        try:
            user_teams_key = self.user_teams_keys_repository.add_key(
                new_key.to_entity()
            )

            return UserTeamKeyDTO(
                id=uuid.UUID(str(user_teams_key.id)),
                user_id=uuid.UUID(str(user_teams_key.user_id)),
                team_id=uuid.UUID(str(user_teams_key.team_id)),
                team_key_encrypted=str(user_teams_key.team_key_encrypted),
            )

        except Exception as e:
            raise UserTeamKeyAdditionException(str(e)) from e


class GetUserTeamKeyByIdUseCase:
    def __init__(self, UserTeamKeyRepository: IUserTeamKeyService):
        self.user_teams_keys_repository = UserTeamKeyRepository

    def execute(self, key_id: uuid.UUID) -> UserTeamKeyDTO:
        try:
            key = self.user_teams_keys_repository.get_key_by_id(key_id)
            return UserTeamKeyDTO(
                id=uuid.UUID(str(key.id)),
                user_id=uuid.UUID(str(key.user_id)),
                team_id=uuid.UUID(str(key.team_id)),
                team_key_encrypted=str(key.team_key_encrypted),
            )

        except Exception as e:
            raise UserTeamKeyRetrievalByIdException(str(e)) from e


class GetUserTeamKeysByTeamIdUseCase:
    def __init__(self, UserTeamKeyRepository: IUserTeamKeyService):
        self.user_teams_keys_repository = UserTeamKeyRepository

    def execute(self, team_id: uuid.UUID) -> list[UserTeamKeyDTO]:
        try:
            keys = self.user_teams_keys_repository.get_keys_by_team_id(team_id)
            return [
                UserTeamKeyDTO(
                    id=uuid.UUID(str(key.id)),
                    user_id=uuid.UUID(str(key.user_id)),
                    team_id=uuid.UUID(str(key.team_id)),
                    team_key_encrypted=str(key.team_key_encrypted),
                )
                for key in keys
            ]

        except Exception as e:
            raise UserTeamKeysRetrievalByTeamIdException(str(e)) from e


class GetUserTeamKeysByUserIdUseCase:
    def __init__(self, UserTeamKeyRepository: IUserTeamKeyService):
        self.user_teams_keys_repository = UserTeamKeyRepository

    def execute(self, user_id: uuid.UUID) -> list[UserTeamKeyDTO]:
        try:
            keys = self.user_teams_keys_repository.get_keys_by_user_id(user_id)
            return [
                UserTeamKeyDTO(
                    id=uuid.UUID(str(key.id)),
                    user_id=uuid.UUID(str(key.user_id)),
                    team_id=uuid.UUID(str(key.team_id)),
                    team_key_encrypted=str(key.team_key_encrypted),
                )
                for key in keys
            ]

        except Exception as e:
            raise UserTeamKeysRetrievalByUserIdException(str(e)) from e


class UpdateUserTeamKeyUseCase:
    def __init__(self, UserTeamKeyRepository: IUserTeamKeyService):
        self.user_teams_keys_repository = UserTeamKeyRepository

    def execute(
        self, interactor_id: uuid.UUID, new_key_data: UpdateUserTeamKeyDTO
    ) -> UserTeamKeyDTO:
        try:
            existing_key = self.user_teams_keys_repository.get_keys_by_user_id(
                new_key_data.user_id
            )
            existing_key = next(
                (
                    k
                    for k in existing_key
                    if str(k.team_id) == str(new_key_data.team_id)
                ),
                None,
            )
            if not existing_key:
                raise Exception("Key not found for this user in this team.")

            updated_key = self.user_teams_keys_repository.update_key(
                new_key_data.to_entity(existing_key)
            )

            return UserTeamKeyDTO(
                id=uuid.UUID(str(updated_key.id)),
                user_id=uuid.UUID(str(updated_key.user_id)),
                team_id=uuid.UUID(str(updated_key.team_id)),
                team_key_encrypted=str(updated_key.team_key_encrypted),
            )

        except Exception as e:
            raise UserTeamKeyUpdateException(str(e)) from e


class RemoveUserTeamKeyUseCase:
    def __init__(self, UserTeamKeyRepository: IUserTeamKeyService):
        self.user_teams_keys_repository = UserTeamKeyRepository

    def execute(
        self, interactor_id: uuid.UUID, key_to_delete: RemoveUserTeamKeyDTO
    ) -> dict[str, str]:
        try:
            removal_result = self.user_teams_keys_repository.remove_key(
                user_id=key_to_delete.user_id, team_id=key_to_delete.team_id
            )

            return removal_result

        except Exception as e:
            raise UserTeamKeyRemovalException(str(e)) from e
