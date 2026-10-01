from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from infrastructure.databases.base import Base
# ORM mappings live in infrastructure now, not domain, so they have to be
# imported explicitly here to register their tables on Base.metadata.
import infrastructure.databases.models.user_model  # noqa: F401
import infrastructure.databases.models.team_model  # noqa: F401
import infrastructure.databases.models.team_perm_level_model  # noqa: F401
import infrastructure.databases.models.team_member_model  # noqa: F401
import infrastructure.databases.models.sub_account_model  # noqa: F401
import infrastructure.databases.models.categories_model  # noqa: F401
import infrastructure.databases.models.sub_account_categories_model  # noqa: F401
import infrastructure.databases.models.user_favorite_model  # noqa: F401
import infrastructure.databases.models.user_teams_keys_model  # noqa: F401
import infrastructure.databases.models.sub_account_history_model  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def run_migrations_offline() -> None:
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL  
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
