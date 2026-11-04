from pydantic import BaseModel, UUID4
from typing import Optional

from domain.entities.team_perm_level import TeamPermLevel


class TeamPermLevelDTO(BaseModel):
    id: UUID4
    team_id: UUID4
    name: str
    rank: int

    def to_entity(self) -> TeamPermLevel:
        return TeamPermLevel(team_id=self.team_id, name=self.name, rank=self.rank)


class CreateTeamPermLevelDTO(BaseModel):
    team_id: UUID4
    name: str
    rank: int

    def to_entity(self) -> TeamPermLevel:
        return TeamPermLevel(team_id=self.team_id, name=self.name, rank=self.rank)


class UpdateTeamPermLevelDTO(BaseModel):
    name: Optional[str] = None
    rank: Optional[int] = None

    def to_entity(self, existing_perm_level: TeamPermLevel) -> TeamPermLevel:
        return TeamPermLevel(
            team_id=existing_perm_level.team_id,
            name=self.name if self.name is not None else existing_perm_level.name,
            rank=self.rank if self.rank is not None else existing_perm_level.rank,
        )
