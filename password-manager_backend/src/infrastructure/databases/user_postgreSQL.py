from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.user_postrgreSQL_exceptions import *

from domain.interfaces.user_service_interface import IUserService
from domain.entities.user import User
from infrastructure.databases.models.user_model import UserModel


def _to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        keycloak_id=model.keycloak_id,
        username=model.username,
        code=model.code,
        salt=model.salt,
        public_key_ec=model.public_key_ec,
        private_key_ec=model.private_key_ec,
        public_key_pq=model.public_key_pq,
        private_key_pq=model.private_key_pq,
    )


class UserService(IUserService):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, new_user: User) -> User:
        try:
            user_model = UserModel(
                username=new_user.username,
                code=new_user.code,
                salt=new_user.salt,
                public_key_ec=new_user.public_key_ec,
                private_key_ec=new_user.private_key_ec,
                public_key_pq=new_user.public_key_pq,
                private_key_pq=new_user.private_key_pq,
            )
            if new_user.id is not None:
                user_model.id = new_user.id
            if new_user.keycloak_id is not None:
                user_model.keycloak_id = new_user.keycloak_id

            self.db.add(user_model)
            self.db.flush()
            self.db.refresh(user_model)

            return _to_domain(user_model)

        except IntegrityError:
            raise UserAlreadyExistsException()

        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserCreationFailedException()

    def get_user_by_keycloak_id(self, keycloak_user_id: uuid.UUID):
        try:
            user_model = (
                self.db.query(UserModel)
                .filter(UserModel.keycloak_id == keycloak_user_id)
                .first()
            )
            if not user_model:
                raise UserNotFoundException(
                    f"User with keycloak_id {keycloak_user_id} not found."
                )
            return _to_domain(user_model)

        except UserNotFoundException:
            raise

        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetUserByIdRetrivalException()

    def get_user_by_username_and_code(self, username: str, code: str):
        try:
            user_model = (
                self.db.query(UserModel)
                .filter(UserModel.username == username, UserModel.code == code)
                .first()
            )
            if not user_model:
                raise UserNotFoundException(
                    f"User with username {username} and code {code} not found."
                )
            return _to_domain(user_model)

        except UserNotFoundException:
            raise

        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetUserByIdRetrivalException()

    def get_user_by_id(self, user_id: uuid.UUID):
        try:
            user_model = (
                self.db.query(UserModel).filter(UserModel.id == user_id).first()
            )
            if not user_model:
                raise UserNotFoundException(f"User with id {user_id} not found.")
            return _to_domain(user_model)

        except UserNotFoundException:
            raise

        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetUserByIdRetrivalException()

    def update_user_by_id(self, user_id: uuid.UUID, new_user: User):
        try:
            user_model = (
                self.db.query(UserModel).filter(UserModel.id == user_id).first()
            )
            if not user_model:
                raise UserNotFoundException("User not found.")

            for key, value in new_user.__dict__.items():
                if not key.startswith("_") and value is not None:
                    setattr(user_model, key, value)

            self.db.flush()
            self.db.refresh(user_model)

            return _to_domain(user_model)

        except UserNotFoundException:
            raise

        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserUpdateFailedException()

    def delete_user_by_id(self, user_id: uuid.UUID) -> dict[str, str]:
        try:
            user_model = (
                self.db.query(UserModel).filter(UserModel.id == user_id).first()
            )
            if not user_model:
                raise UserNotFoundException("User not found.")

            self.db.delete(user_model)

            return {"message": "User deleted successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserDeleteException()
