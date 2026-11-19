
"""Insert data into products table

Revision ID: ac1c2663f9e5
Revises: 78f11c39a447
"""

from alembic import op
import sqlalchemy as sa


revision = 'ac1c2663f9e5'
down_revision = '78f11c39a447'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    categories_table = sa.table(
        'categories',
        sa.column('name', sa.String(100))
    )

    products_table = sa.table(
        'products',
        sa.column('name', sa.String(100)),
        sa.column('price', sa.Float()),
        sa.column('active', sa.Boolean()),
        sa.column('category_id', sa.Integer())
    )

    op.bulk_insert(
        categories_table,
        [
            {'name': 'Books'},
            {'name': 'Clothing'}
        ]
    )

    books_id = connection.execute(
        sa.text("SELECT id FROM categories WHERE name = 'Books'")
    ).scalar_one()

    clothing_id = connection.execute(
        sa.text("SELECT id FROM categories WHERE name = 'Clothing'")
    ).scalar_one()

    op.bulk_insert(
        products_table,
        [
            {
                'name': 'Smartphone',
                'price': 799.99,
                'active': True,
                'category_id': None
            },
            {
                'name': 'Novel',
                'price': 19.99,
                'active': True,
                'category_id': books_id
            },
            {
                'name': 'T-Shirt',
                'price': 29.99,
                'active': True,
                'category_id': clothing_id
            }
        ]
    )


def downgrade():
    connection = op.get_bind()

    connection.execute(
        sa.text(
            "DELETE FROM products "
            "WHERE name IN ('Smartphone', 'Novel', 'T-Shirt')"
        )
    )

    connection.execute(
        sa.text(
            "DELETE FROM categories "
            "WHERE name IN ('Books', 'Clothing')"
        )
    )
