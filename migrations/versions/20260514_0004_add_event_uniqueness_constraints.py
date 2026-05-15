"""add event uniqueness constraints

Revision ID: 20260514_0004
Revises: 20260514_0003
Create Date: 2026-05-14 00:00:04
"""

from __future__ import annotations

from alembic import op


# revision identifiers, used by Alembic.
revision = "20260514_0004"
down_revision = "20260514_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("events") as batch_op:
        batch_op.create_unique_constraint("uq_events_title", ["title"])
        batch_op.create_unique_constraint("uq_events_description", ["description"])
        batch_op.create_unique_constraint(
            "uq_events_date_location",
            ["date", "location"],
        )


def downgrade() -> None:
    with op.batch_alter_table("events") as batch_op:
        batch_op.drop_constraint("uq_events_date_location", type_="unique")
        batch_op.drop_constraint("uq_events_description", type_="unique")
        batch_op.drop_constraint("uq_events_title", type_="unique")
