import uuid

from sqlalchemy import String, ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.databases.base import Base


class CategoriesModel(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("team_id", "name", name="uq_categories_team_id_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
