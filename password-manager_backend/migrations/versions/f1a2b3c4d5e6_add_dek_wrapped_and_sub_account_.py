"""add dek_wrapped and sub_account_history table

Revision ID: f1a2b3c4d5e6
Revises: 3713186a3cdb
Create Date: 2026-10-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, None] = '3713186a3cdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('sub_accounts', sa.Column('dek_wrapped', sa.String(), nullable=True))

    op.create_table(
        'sub_account_history',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('sub_account_id', sa.UUID(), nullable=False),
        sa.Column('username_encrypted', sa.String(length=100), nullable=True),
        sa.Column('email_encrypted', sa.String(length=255), nullable=True),
        sa.Column('password_encrypted', sa.String(), nullable=False),
        sa.Column('site_link_encrypted', sa.String(length=255), nullable=True),
        sa.Column('dek_wrapped', sa.String(), nullable=True),
        sa.Column('changed_by', sa.UUID(), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['sub_account_id'], ['sub_accounts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['changed_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sub_account_history')
    op.drop_column('sub_accounts', 'dek_wrapped')
