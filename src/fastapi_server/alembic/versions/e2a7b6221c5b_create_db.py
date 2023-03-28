"""Create db

Revision ID: e2a7b6221c5b
Revises: 
Create Date: 2023-03-24 17:26:02.668526

"""
from alembic import op
import sqlalchemy as sa
import os
from src.fastapi_server.services.users import UsersService


# revision identifiers, used by Alembic.
revision = 'e2a7b6221c5b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password_hashed', sa.String(), nullable=True),
    sa.Column('role', sa.Enum('admin', 'viewer', name='roleenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('responses_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request', sa.Enum('preprocessing', 'fit', 'predict', 'download', name='requestenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.drop_table('responses_history')
    op.drop_table('users')
    # ### end Alembic commands ###
