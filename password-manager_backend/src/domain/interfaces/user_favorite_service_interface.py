import uuid
from abc import ABC, abstractmethod

from domain.entities.user_favorite import UserFavorite


@abstractmethod
class IUserFavoriteService(ABC):
    @abstractmethod
    def add_favorite(self, new_favorite: UserFavorite) -> UserFavorite:
        pass

    @abstractmethod
    def remove_favorite(
        self, user_id: uuid.UUID, sub_account_id: uuid.UUID
    ) -> dict[str, str]:
        pass

    @abstractmethod
    def get_favorites_by_user_id(self, user_id: uuid.UUID) -> list[UserFavorite]:
        pass
