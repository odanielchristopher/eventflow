from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from src.models.checkin.schemas import CheckInRead


class SubscriptionBase(SQLModel):
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    price: Decimal = Field(decimal_places=2, max_digits=10)
    registered_at: date_type = Field(default_factory=date_type.today)
    event_id: int


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    price: Decimal | None = Field(default=None, decimal_places=2, max_digits=10)
    registered_at: date_type | None = None
    event_id: int | None = None


class SubscriptionRead(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    check_in: CheckInRead | None = None
