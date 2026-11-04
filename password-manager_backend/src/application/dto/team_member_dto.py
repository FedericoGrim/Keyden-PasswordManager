from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from domain.entities.team_member import TeamMember


class TeamMemberDTO(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    perm_level_id: UUID

    def to_entity(self) -> TeamMember:
        return TeamMember(
            user_id=self.user_id, team_id=self.team_id, perm_level_id=self.perm_level_id
        )


class CreateTeamMemberDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    perm_level_id: UUID

    def to_entity(self) -> TeamMember:
        return TeamMember(
            user_id=self.user_id, team_id=self.team_id, perm_level_id=self.perm_level_id
        )


class UpdateTeamMemberDTO(BaseModel):
    user_id: UUID
    team_id: UUID
    perm_level_id: Optional[UUID]

    def to_entity(self, existing_member: TeamMember) -> TeamMember:
        return TeamMember(
            user_id=UUID(str(existing_member.user_id)),
            team_id=UUID(str(existing_member.team_id)),
            perm_level_id=self.perm_level_id
            if self.perm_level_id is not None
            else existing_member.perm_level_id,
        )


class RemoveTeamMemberDTO(BaseModel):
    member_id: UUID
    team_id: UUID
