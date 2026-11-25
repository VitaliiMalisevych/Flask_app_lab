
"""Add author relationship to posts

Revision ID: f736e58dccb2
Revises: 54a2b2fd354e
"""

from alembic import op
import sqlalchemy as sa


revision = "f736e58dccb2"
down_revision = "54a2b2fd354e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("posts") as batch_op:
        batch_op.add_column(
            sa.Column(
                "author_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            "fk_posts_author_id_users",
            "users",
            ["author_id"],
            ["id"]
        )


def downgrade():
    with op.batch_alter_table("posts") as batch_op:
        batch_op.drop_constraint(
            "fk_posts_author_id_users",
            type_="foreignkey"
        )

        batch_op.drop_column("author_id")
