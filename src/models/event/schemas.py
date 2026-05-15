from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal
from typing import Annotated

from fastapi import Form
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from src.models.document.schemas import DocumentRead


class EventBase(SQLModel):
    title: str = Field(max_length=255)
    description: str = Field(max_length=1000)
    banner_img_url: str | None = Field(default=None, max_length=500)
    date: date_type
    location: str = Field(max_length=255)
    capacity: int = Field(gt=0)
    sub_price: Decimal = Field(decimal_places=2, max_digits=10)


class EventCreate(EventBase):
    @classmethod
    def as_form(
        cls,
        title: Annotated[str, Form()],
        description: Annotated[str, Form()],
        date: Annotated[date_type, Form()],
        location: Annotated[str, Form()],
        capacity: Annotated[int, Form()],
        sub_price: Annotated[Decimal, Form()],
    ) -> "EventCreate":
        return cls(
            title=title,
            description=description,
            date=date,
            location=location,
            capacity=capacity,
            sub_price=sub_price,
        )


class EventUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    banner_img_url: str | None = Field(default=None, max_length=500)
    date: date_type | None = None
    location: str | None = Field(default=None, max_length=255)
    capacity: int | None = Field(default=None, gt=0)
    sub_price: Decimal | None = Field(default=None, decimal_places=2, max_digits=10)

    @classmethod
    def as_form(
        cls,
        title: Annotated[str | None, Form()] = None,
        description: Annotated[str | None, Form()] = None,
        date: Annotated[date_type | None, Form()] = None,
        location: Annotated[str | None, Form()] = None,
        capacity: Annotated[int | None, Form()] = None,
        sub_price: Annotated[Decimal | None, Form()] = None,
    ) -> "EventUpdate":
        return cls(
            title=title,
            description=description,
            date=date,
            location=location,
            capacity=capacity,
            sub_price=sub_price,
        )


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    documents: list[DocumentRead] = Field(default_factory=list)
