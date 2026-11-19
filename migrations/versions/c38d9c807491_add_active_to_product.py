
"""Add active to Product

Revision ID: c38d9c807491
Revises: 7c5755548aac
Create Date: 2026-11-19 08:26:57.231326
"""

from alembic import op
import sqlalchemy as sa


revision = 'c38d9c807491'
down_revision = '7c5755548aac'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'active',
                sa.Boolean(),
                nullable=False,
                server_default=sa.true()
            )
        )


def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('active')
