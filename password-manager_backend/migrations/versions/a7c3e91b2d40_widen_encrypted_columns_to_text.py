"""widen encrypted columns to text

Revision ID: a7c3e91b2d40
Revises: f1a2b3c4d5e6
Create Date: 2026-11-06 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7c3e91b2d40"
down_revision: Union[str, None] = "f1a2b3c4d5e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLES = ("sub_accounts", "sub_account_history")
COLUMNS = {
    "username_encrypted": 100,
    "email_encrypted": 255,
    "site_link_encrypted": 255,
}


def upgrade() -> None:
    """Upgrade schema."""
    for table in TABLES:
        for column in COLUMNS:
            op.alter_column(
                table,
                column,
                existing_type=sa.String(),
                type_=sa.Text(),
                existing_nullable=True,
            )


def downgrade() -> None:
    """Downgrade schema."""
    for table in TABLES:
        for column, length in COLUMNS.items():
            op.alter_column(
                table,
                column,
                existing_type=sa.Text(),
                type_=sa.String(length=length),
                existing_nullable=True,
            )
