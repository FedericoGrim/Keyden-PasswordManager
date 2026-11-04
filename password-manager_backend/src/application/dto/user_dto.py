from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from domain.entities.user import User
from domain.generate_user_code import USER_CODE_LENGTH


class UserDTO(BaseModel):
    id: UUID | None
    keycloak_id: UUID | None

    username: str
    code: str

    salt: str

    public_key_ec: bytes
    private_key_ec: bytes

    public_key_pq: bytes
    private_key_pq: bytes

    @classmethod
    def from_entity(cls, entity: User) -> "UserDTO":
        return cls(
            id=entity.id,
            keycloak_id=entity.keycloak_id,
            username=entity.username,
            code=entity.code,
            salt=entity.salt,
            public_key_ec=entity.public_key_ec,
            private_key_ec=entity.private_key_ec,
            public_key_pq=entity.public_key_pq,
            private_key_pq=entity.private_key_pq,
        )

    def to_entity(self) -> User:
        return User(
            keycloak_id=self.keycloak_id,
            username=self.username,
            code=self.code,
            salt=self.salt,
            public_key_ec=self.public_key_ec,
            private_key_ec=self.private_key_ec,
            public_key_pq=self.public_key_pq,
            private_key_pq=self.private_key_pq,
        )


class CreateUserDTO(BaseModel):
    id: UUID
    keycloak_id: UUID
    username: str
    code: str = Field(
        min_length=USER_CODE_LENGTH,
        max_length=USER_CODE_LENGTH,
        pattern=r"^[A-Za-z0-9]+$",
    )

    salt: str

    public_key_ec: bytes
    private_key_ec: bytes

    public_key_pq: bytes
    private_key_pq: bytes

    team_key_encrypted: str

    def to_entity(self) -> User:
        return User(
            id=self.id,
            keycloak_id=self.keycloak_id,
            username=self.username,
            code=self.code,
            salt=self.salt,
            public_key_ec=self.public_key_ec,
            private_key_ec=self.private_key_ec,
            public_key_pq=self.public_key_pq,
            private_key_pq=self.private_key_pq,
        )


class UserPublicDTO(BaseModel):
    id: UUID | None
    username: str
    code: str

    public_key_ec: bytes
    public_key_pq: bytes

    @classmethod
    def from_entity(cls, entity: User) -> "UserPublicDTO":
        return cls(
            id=entity.id,
            username=entity.username,
            code=entity.code,
            public_key_ec=entity.public_key_ec,
            public_key_pq=entity.public_key_pq,
        )


class UpdateUserDTO(BaseModel):
    keycloak_id: Optional[UUID]
    username: Optional[str]

    salt: Optional[str]

    public_key_ec: Optional[bytes]
    private_key_ec: Optional[bytes]

    public_key_pq: Optional[bytes]
    private_key_pq: Optional[bytes]

    def to_entity(self, existing_user: User) -> User:
        return User(
            id=existing_user.id,
            keycloak_id=self.keycloak_id
            if self.keycloak_id is not None
            else existing_user.keycloak_id,
            username=self.username
            if self.username is not None
            else existing_user.username,
            code=existing_user.code,
            salt=self.salt if self.salt is not None else existing_user.salt,
            public_key_ec=self.public_key_ec
            if self.public_key_ec is not None
            else existing_user.public_key_ec,
            private_key_ec=self.private_key_ec
            if self.private_key_ec is not None
            else existing_user.private_key_ec,
            public_key_pq=self.public_key_pq
            if self.public_key_pq is not None
            else existing_user.public_key_pq,
            private_key_pq=self.private_key_pq
            if self.private_key_pq is not None
            else existing_user.private_key_pq,
        )
