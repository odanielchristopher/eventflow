from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.subscription.entity import Subscription


class CheckIn(SQLModel, table=True):
    __tablename__ = "check_ins"
    __table_args__ = (
        UniqueConstraint("subscription_id", name="uq_check_ins_subscription_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(sa_column=Column(DateTime(), nullable=False))
    access_point: str = Field(sa_column=Column(String(length=255), nullable=False))
    subscription_id: int = Field(foreign_key="subscriptions.id", nullable=False)

    subscription: "Subscription" = Relationship(back_populates="check_in")
