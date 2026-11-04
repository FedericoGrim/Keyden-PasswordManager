from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from domain.entities.user_teams_keys import UserTeamKey


class UserTeamKeyDTO(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    team_key_encrypted: str

    def to_entity(self) -> UserTeamKey:
        return UserTeamKey(
            user_id=self.user_id,
            team_id=self.team_id,
            team_key_encrypted=self.team_key_encrypted,
        )


class CreateUserTeamKeyDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    team_key_encrypted: str

    def to_entity(self) -> UserTeamKey:
        return UserTeamKey(
            user_id=self.user_id,
            team_id=self.team_id,
            team_key_encrypted=self.team_key_encrypted,
        )


class UpdateUserTeamKeyDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    team_key_encrypted: Optional[str]

    def to_entity(self, existing_key: UserTeamKey) -> UserTeamKey:
        return UserTeamKey(
            user_id=UUID(str(existing_key.user_id)),
            team_id=UUID(str(existing_key.team_id)),
            team_key_encrypted=self.team_key_encrypted
            if self.team_key_encrypted is not None
            else existing_key.team_key_encrypted,
        )


class RemoveUserTeamKeyDTO(BaseModel):
    user_id: UUID
    team_id: UUID
