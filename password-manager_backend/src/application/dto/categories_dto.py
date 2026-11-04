from pydantic import BaseModel, UUID4
from typing import Optional

from domain.entities.categories import Category


class CategoryDTO(BaseModel):
    id: UUID4
    team_id: UUID4
    name: str

    def to_entity(self) -> Category:
        return Category(team_id=self.team_id, name=self.name)


class CreateCategoryDTO(BaseModel):
    team_id: UUID4
    name: str

    def to_entity(self) -> Category:
        return Category(team_id=self.team_id, name=self.name)


class UpdateCategoryDTO(BaseModel):
    name: Optional[str] = None

    def to_entity(self) -> Category:
        return Category(name=self.name)
