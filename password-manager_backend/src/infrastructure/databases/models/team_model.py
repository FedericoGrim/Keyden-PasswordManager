import uuid

from sqlalchemy import Boolean, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.databases.base import Base


class TeamModel(Base):
    __tablename__ = "teams"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_personal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
