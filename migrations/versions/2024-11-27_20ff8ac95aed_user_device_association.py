"""user-device association

Revision ID: 20ff8ac95aed
Revises: de7849c6bb8d
Create Date: 2024-11-27 09:31:50.146139

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20ff8ac95aed"
down_revision = "de7849c6bb8d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_device",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("device_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["devices.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
    )


def downgrade():
    op.drop_table("user_device")
