
"""Add created_at to Product

Revision ID: 78f11c39a447
Revises: c38d9c807491
Create Date: 2026-11-19 08:32:42.635522
"""

from alembic import op
import sqlalchemy as sa


revision = '78f11c39a447'
down_revision = 'c38d9c807491'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        'products',
        schema=None,
        recreate='always'
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                'created_at',
                sa.DateTime(timezone=True),
                server_default=sa.text('(CURRENT_TIMESTAMP)'),
                nullable=False
            )
        )


def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('created_at')
