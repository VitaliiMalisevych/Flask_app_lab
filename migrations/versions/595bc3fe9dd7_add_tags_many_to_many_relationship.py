
from alembic import op
import sqlalchemy as sa


revision = "595bc3fe9dd7"
down_revision = "f736e58dccb2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name")
    )

    op.create_table(
        "post_tags",
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"]
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"]
        ),
        sa.PrimaryKeyConstraint("post_id", "tag_id")
    )


def downgrade():
    op.drop_table("post_tags")
    op.drop_table("tags")
