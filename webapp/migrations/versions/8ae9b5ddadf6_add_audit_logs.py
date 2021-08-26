"""add audit logs

Revision ID: 8ae9b5ddadf6
Revises: e9fbe7694450
Create Date: 2021-04-22 12:06:35.642688

"""
from alembic import op
import sqlalchemy as sa

from flask import current_app

# revision identifiers, used by Alembic.
revision = '8ae9b5ddadf6'
down_revision = 'e9fbe7694450'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('audit_log',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('log_data', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    if current_app.config['ENV'] in ('staging', 'production'):
        # only INSERT allowed
        op.execute("""
        GRANT INSERT ON TABLE "audit_log" TO steuerlotse;
        GRANT ALL ON SEQUENCE audit_log_id_seq TO steuerlotse;
        """)


def downgrade():
    op.drop_table('audit_log')
