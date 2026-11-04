import uuid
from abc import ABC, abstractmethod

from domain.entities.user import User


@abstractmethod
class IUserService(ABC):
    @abstractmethod
    def create_user(self, new_user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_keycloak_id(self, keycloak_user_id: uuid.UUID) -> User:
        pass

    @abstractmethod
    def get_user_by_username_and_code(self, username: str, code: str) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: uuid.UUID) -> User:
        pass

    @abstractmethod
    def update_user_by_id(self, user_id: uuid.UUID, new_user: User) -> User:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: uuid.UUID) -> dict[str, str]:
        pass
