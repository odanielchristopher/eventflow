from datetime import date as date_type
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, Numeric, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.event.entity import Event


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(length=255), nullable=False))
    email: str = Field(sa_column=Column(String(length=255), nullable=False))
    price: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    registered_at: date_type = Field(sa_column=Column(Date(), nullable=False))
    event_id: int = Field(foreign_key="events.id", nullable=False)

    event: "Event" = Relationship(back_populates="subscriptions")
