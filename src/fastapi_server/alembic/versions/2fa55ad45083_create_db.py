"""Create db

Revision ID: 2fa55ad45083
Revises: 232183331d80
Create Date: 2023-03-27 17:31:57.322154

"""
from alembic import op
import sqlalchemy as sa
import os
from src.fastapi_server.services.users import UsersService


# revision identifiers, used by Alembic.
revision = '2fa55ad45083'
down_revision = '232183331d80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
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
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
