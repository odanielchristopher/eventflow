from __future__ import annotations

from bson.decimal128 import Decimal128
from datetime import date as date_type
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.models.checkin.schemas import CheckInCreate, CheckInRead, CheckInUpdate


class SubscriptionBase(BaseModel):
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    price: Decimal = Field(decimal_places=2, max_digits=10)
    registered_at: date_type = Field(default_factory=date_type.today)

    @field_validator("price", mode="before")
    @classmethod
    def normalize_price(cls, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    price: Decimal | None = Field(default=None, decimal_places=2, max_digits=10)
    registered_at: date_type | None = None
    check_in: CheckInCreate | CheckInUpdate | None = None

    @field_validator("price", mode="before")
    @classmethod
    def normalize_price(cls, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value


class SubscriptionRead(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    check_in: CheckInRead | None = None

    @field_validator("id", mode="before")
    @classmethod
    def stringify_ids(cls, value) -> str:
        return str(value)


class SubscriptionCheckInCountRead(BaseModel):
    count: int = Field(ge=0)
