from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from domain.entities.team import Team


class TeamDTO(BaseModel):
    id: UUID
    name: str
    is_personal: bool

    def to_entity(self) -> Team:
        return Team(id=self.id, name=self.name, is_personal=self.is_personal)


class CreateTeamDTO(BaseModel):
    name: str

    def to_entity(self) -> Team:
        return Team(name=self.name)


class UpdateTeamDTO(BaseModel):
    id: UUID
    name: Optional[str]

    def to_entity(self, existing_team: Team) -> Team:
        return Team(
            id=existing_team.id,
            name=self.name if self.name is not None else existing_team.name,
            is_personal=existing_team.is_personal,
        )


class DeleteTeamDTO(BaseModel):
    id: UUID
