import uuid

from sqlalchemy import ForeignKey, Integer, String, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.databases.base import Base


class TeamPermLevelModel(Base):
    __tablename__ = "team_perm_levels"
    __table_args__ = (
        UniqueConstraint("team_id", "name", name="uq_team_perm_levels_team_id_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
