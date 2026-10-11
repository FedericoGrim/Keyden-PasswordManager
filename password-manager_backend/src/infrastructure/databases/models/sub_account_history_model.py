import uuid
from datetime import datetime

from sqlalchemy import String, UUID, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.databases.base import Base


class SubAccountHistoryModel(Base):
    """SQLAlchemy mapping for `sub_account_history`. Persistence shape only —
    the business object is domain.entities.sub_account_history.SubAccountHistory."""

    __tablename__ = "sub_account_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    sub_account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sub_accounts.id", ondelete="CASCADE"), nullable=False)
    username_encrypted: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email_encrypted: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_encrypted: Mapped[str] = mapped_column(String, nullable=False)
    site_link_encrypted: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dek_wrapped: Mapped[str | None] = mapped_column(String, nullable=True)
    changed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
