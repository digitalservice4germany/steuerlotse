"""Add required grants

Revision ID: e9fbe7694450
Revises: c0b039d92792
Create Date: 2021-04-19 12:59:52.861502

"""
from alembic import op
import sqlalchemy as sa

from flask import current_app


# revision identifiers, used by Alembic.
revision = 'e9fbe7694450'
down_revision = 'c0b039d92792'
branch_labels = None
depends_on = None


def upgrade():
    if current_app.config['ENV'] in ('staging', 'production'):
        op.execute("""
        GRANT ALL ON TABLE "user" TO steuerlotse;
        GRANT ALL ON SEQUENCE user_id_seq TO steuerlotse;
        """)


def downgrade():
    pass
