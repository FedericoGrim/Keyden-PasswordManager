import uuid

from application.exceptions.user_favorite_use_case_exceptions import (
    UserFavoriteAdditionException,
    UserFavoriteRemovalException,
    UserFavoriteRetrievalException,
)
from application.dto.user_favorite_dto import FavoriteDTO, CreateFavoriteDTO

from domain.interfaces.user_favorite_service_interface import IUserFavoriteService


class AddFavoriteUseCase:
    def __init__(self, UserFavoriteRepository: IUserFavoriteService) -> None:
        self.user_favorite_repository = UserFavoriteRepository

    def execute(self, new_favorite: CreateFavoriteDTO) -> FavoriteDTO:
        try:
            favorite = self.user_favorite_repository.add_favorite(
                new_favorite.to_entity()
            )

            return FavoriteDTO(
                id=uuid.UUID(str(favorite.id)),
                user_id=uuid.UUID(str(favorite.user_id)),
                sub_account_id=uuid.UUID(str(favorite.sub_account_id)),
            )

        except Exception as e:
            raise UserFavoriteAdditionException(str(e)) from e


class GetFavoritesByUserIdUseCase:
    def __init__(self, UserFavoriteRepository: IUserFavoriteService) -> None:
        self.user_favorite_repository = UserFavoriteRepository

    def execute(self, user_id: uuid.UUID) -> list[FavoriteDTO]:
        try:
            favorites = self.user_favorite_repository.get_favorites_by_user_id(user_id)
            return [
                FavoriteDTO(
                    id=uuid.UUID(str(fav.id)),
                    user_id=uuid.UUID(str(fav.user_id)),
                    sub_account_id=uuid.UUID(str(fav.sub_account_id)),
                )
                for fav in favorites
            ]

        except Exception as e:
            raise UserFavoriteRetrievalException(str(e)) from e


class RemoveFavoriteUseCase:
    def __init__(self, UserFavoriteRepository: IUserFavoriteService) -> None:
        self.user_favorite_repository = UserFavoriteRepository

    def execute(self, user_id: uuid.UUID, sub_account_id: uuid.UUID) -> dict[str, str]:
        try:
            return self.user_favorite_repository.remove_favorite(
                user_id, sub_account_id
            )

        except Exception as e:
            raise UserFavoriteRemovalException(str(e)) from e
