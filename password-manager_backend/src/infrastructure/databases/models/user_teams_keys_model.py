import uuid

from sqlalchemy import String, ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.databases.base import Base


class UserTeamKeyModel(Base):
    __tablename__ = "user_teams_keys"
    __table_args__ = (
        UniqueConstraint(
            "team_id", "user_id", name="uq_user_teams_keys_team_id_user_id"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    team_key_encrypted: Mapped[str] = mapped_column(String, nullable=False)
