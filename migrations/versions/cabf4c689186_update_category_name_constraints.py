
"""Update Category name constraints

Revision ID: cabf4c689186
Revises: ac1c2663f9e5
Create Date: 2026-11-19 08:41:27.927510
"""

from alembic import op
import sqlalchemy as sa


revision = 'cabf4c689186'
down_revision = 'ac1c2663f9e5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        'categories',
        schema=None,
        recreate='always'
    ) as batch_op:
        batch_op.alter_column(
            'name',
            existing_type=sa.VARCHAR(length=100),
            type_=sa.String(length=128),
            existing_nullable=False
        )

        batch_op.create_unique_constraint(
            batch_op.f('uq_categories_name'),
            ['name']
        )


def downgrade():
    with op.batch_alter_table(
        'categories',
        schema=None,
        recreate='always'
    ) as batch_op:
        batch_op.drop_constraint(
            batch_op.f('uq_categories_name'),
            type_='unique'
        )

        batch_op.alter_column(
            'name',
            existing_type=sa.String(length=128),
            type_=sa.VARCHAR(length=100),
            existing_nullable=False
        )
