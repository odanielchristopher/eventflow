from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class EventBase(SQLModel):
    title: str = Field(max_length=255)
    description: str = Field(max_length=1000)
    banner_img_url: str | None = Field(default=None, max_length=500)
    date: date_type
    location: str = Field(max_length=255)
    capacity: int = Field(gt=0)
    sub_price: Decimal = Field(decimal_places=2, max_digits=10)


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    banner_img_url: str | None = Field(default=None, max_length=500)
    date: date_type | None = None
    location: str | None = Field(default=None, max_length=255)
    capacity: int | None = Field(default=None, gt=0)
    sub_price: Decimal | None = Field(default=None, decimal_places=2, max_digits=10)


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
