"""add subscription email-event uniqueness

Revision ID: 20260514_0006
Revises: 20260514_0005
Create Date: 2026-05-14 00:00:06
"""

from __future__ import annotations

from alembic import op


# revision identifiers, used by Alembic.
revision = "20260514_0006"
down_revision = "20260514_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("subscriptions") as batch_op:
        batch_op.create_unique_constraint(
            "uq_subscriptions_email_event",
            ["email", "event_id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("subscriptions") as batch_op:
        batch_op.drop_constraint("uq_subscriptions_email_event", type_="unique")
