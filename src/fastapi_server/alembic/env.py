import sys
import os
from pathlib import Path
from dotenv import load_dotenv

current_dir = str(Path(os.getcwd()).parent.parent)
if current_dir not in sys.path:
    sys.path.append(current_dir)

dotenv_path = os.path.join(Path(os.getcwd()).parent.parent, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from sqlalchemy import create_engine

from alembic import context

from src.fastapi_server.models import base, user, response_history
from src.fastapi_server.core.settings import settings

target_metadata = base.Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.connection_string
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(
        settings.connection_string
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
