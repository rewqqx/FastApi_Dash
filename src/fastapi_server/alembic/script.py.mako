"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import os
from src.fastapi_server.services.users import UsersService
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}
    # get metadata from current connection
    meta = sa.MetaData()

    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(only=('users',), bind=op.get_bind())

    # define table representation
    some_table_tbl = sa.Table('users', meta)

    con = op.get_bind()
    results = con.execute(sa.text("SELECT id FROM users where role='admin' limit 1"))
    if not results.all():
        op.bulk_insert(
            some_table_tbl,
            [
                {
                    'username': os.environ.get('ADMIN_NAME'),
                    'password_hashed': UsersService.hash_password(os.environ.get('ADMIN_PASSWORD')),
                    'role': 'admin'
                },
            ]
        )


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
