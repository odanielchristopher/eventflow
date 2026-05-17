"""create check ins table

Revision ID: 20260514_0008
Revises: 20260514_0007
Create Date: 2026-05-14 00:00:08
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260514_0008"
down_revision = "20260514_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "check_ins",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("access_point", sa.String(length=255), nullable=False),
        sa.Column("subscription_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["subscription_id"], ["subscriptions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("subscription_id", name="uq_check_ins_subscription_id"),
    )


def downgrade() -> None:
    op.drop_table("check_ins")
