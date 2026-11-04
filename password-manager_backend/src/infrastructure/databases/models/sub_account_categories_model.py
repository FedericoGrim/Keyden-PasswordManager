import uuid

from sqlalchemy import ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.databases.base import Base


class SubAccountCategoriesModel(Base):
    __tablename__ = "sub_account_categories"
    __table_args__ = (
        UniqueConstraint(
            "sub_account_id",
            "category_id",
            name="uq_sub_account_categories_sub_account_id_category_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    sub_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sub_accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
    )
