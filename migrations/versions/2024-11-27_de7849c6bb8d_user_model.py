"""User model

Revision ID: de7849c6bb8d
Revises: afccaca472fa
Create Date: 2024-11-27 08:54:56.345910

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "de7849c6bb8d"
down_revision = "afccaca472fa"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=10), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("users")
