"""Add last_modified column

Revision ID: c0b039d92792
Revises: 2f00a0ea1190
Create Date: 2021-04-06 20:49:22.068992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0b039d92792'
down_revision = '2f00a0ea1190'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('last_modified', sa.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()))


def downgrade():
    op.drop_column('user', 'last_modified')
