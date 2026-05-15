"""link documents to events

Revision ID: 20260514_0003
Revises: 20260514_0002
Create Date: 2026-05-14 00:00:03
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260514_0003"
down_revision = "20260514_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("documents") as batch_op:
        batch_op.add_column(sa.Column("event_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_documents_event_id", ["event_id"], unique=False)
        batch_op.create_foreign_key(
            "fk_documents_event_id_events",
            "events",
            ["event_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("documents") as batch_op:
        batch_op.drop_constraint("fk_documents_event_id_events", type_="foreignkey")
        batch_op.drop_index("ix_documents_event_id")
        batch_op.drop_column("event_id")
