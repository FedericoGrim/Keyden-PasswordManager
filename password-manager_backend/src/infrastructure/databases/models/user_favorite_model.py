import uuid

from sqlalchemy import ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.databases.base import Base


class UserFavoriteModel(Base):
    __tablename__ = "user_favorites"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "sub_account_id", name="uq_user_favorites_user_id_sub_account_id"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    sub_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sub_accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
