"""Initial migration

Revision ID: afccaca472fa
Revises: 
Create Date: 2024-11-25 10:36:28.271761

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "afccaca472fa"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "protection_systems",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("encryption_mode", sa.Enum("aes_ecb", "aes_cbc", name="encryptionmode"), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contents",
        sa.Column("protection_system_id", sa.Integer(), nullable=False),
        sa.Column("encryption_key", sa.LargeBinary(), nullable=False),
        sa.Column("encrypted_payload", sa.LargeBinary(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(["protection_system_id"], ["protection_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "devices",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("protection_system_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(["protection_system_id"], ["protection_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("devices")
    op.drop_table("contents")
    op.drop_table("protection_systems")
    op.execute("DROP TYPE encryptionmode")
