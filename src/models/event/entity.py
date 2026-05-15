from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal

from sqlalchemy import Column, Date, Numeric, String
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(length=255), nullable=False))
    description: str = Field(sa_column=Column(String(length=1000), nullable=False))
    banner_img_url: str | None = Field(
        default=None,
        sa_column=Column(String(length=500), nullable=True),
    )
    date: date_type = Field(sa_column=Column(Date(), nullable=False))
    location: str = Field(sa_column=Column(String(length=255), nullable=False))
    capacity: int = Field(nullable=False, gt=0)
    sub_price: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False),
    )
