import uuid

from sqlalchemy import UUID, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.databases.base import Base
from domain.generate_user_code import USER_CODE_LENGTH


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", "code", name="uq_users_username_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    keycloak_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String(USER_CODE_LENGTH), nullable=False)

    salt: Mapped[str] = mapped_column(String, nullable=False)

    public_key_ec: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    private_key_ec: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    public_key_pq: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    private_key_pq: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
