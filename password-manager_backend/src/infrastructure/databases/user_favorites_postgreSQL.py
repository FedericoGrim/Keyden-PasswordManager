from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging


from domain.interfaces.user_favorite_service_interface import IUserFavoriteService
from domain.entities.user_favorite import UserFavorite
from infrastructure.databases.models.user_favorite_model import UserFavoriteModel


def _to_domain(model: UserFavoriteModel) -> UserFavorite:
    return UserFavorite(
        id=model.id,
        user_id=model.user_id,
        sub_account_id=model.sub_account_id,
    )


class UserFavoritesService(IUserFavoriteService):
    def __init__(self, db: Session) -> None:
        self.Db = db

    def add_favorite(self, new_favorite: UserFavorite) -> UserFavorite:
        try:
            favorite_model = UserFavoriteModel(
                user_id=new_favorite.user_id,
                sub_account_id=new_favorite.sub_account_id,
            )

            self.Db.add(favorite_model)
            self.Db.flush()
            self.Db.refresh(favorite_model)

            return _to_domain(favorite_model)

        except IntegrityError:
            raise Exception("This sub-account is already a favorite.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to add favorite.")

    def remove_favorite(
        self, user_id: uuid.UUID, sub_account_id: uuid.UUID
    ) -> dict[str, str]:
        try:
            favorite_model = (
                self.Db.query(UserFavoriteModel)
                .filter_by(user_id=user_id, sub_account_id=sub_account_id)
                .first()
            )

            if not favorite_model:
                raise Exception("Favorite not found.")

            self.Db.delete(favorite_model)
            self.Db.flush()

            return {"message": "Favorite removed successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to remove favorite.")

    def get_favorites_by_user_id(self, user_id: uuid.UUID) -> list[UserFavorite]:
        try:
            favorite_models = (
                self.Db.query(UserFavoriteModel).filter_by(user_id=user_id).all()
            )
            return [_to_domain(favorite_model) for favorite_model in favorite_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve favorites.")
