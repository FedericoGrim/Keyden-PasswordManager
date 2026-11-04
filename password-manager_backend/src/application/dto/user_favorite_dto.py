from pydantic import BaseModel
from uuid import UUID

from domain.entities.user_favorite import UserFavorite


class FavoriteDTO(BaseModel):
    id: UUID
    user_id: UUID
    sub_account_id: UUID


class CreateFavoriteDTO(BaseModel):
    user_id: UUID
    sub_account_id: UUID

    def to_entity(self) -> UserFavorite:
        return UserFavorite(user_id=self.user_id, sub_account_id=self.sub_account_id)
