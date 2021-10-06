"""Add Timezone to last_modified

Revision ID: 292882794509
Revises: 0cdb4351a66d
Create Date: 2021-05-27 12:07:55.490981

"""
from alembic import op
from flask import current_app
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '292882794509'
down_revision = '0cdb4351a66d'
branch_labels = None
depends_on = None


def upgrade():
    if not current_app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        op.alter_column('user', 'last_modified', type_=sa.TIMESTAMP(timezone=True))

def downgrade():
    pass
