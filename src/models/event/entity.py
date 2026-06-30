from bson.decimal128 import Decimal128
from datetime import date as date_type
from decimal import Decimal

from beanie import Document
from pydantic import Field, field_validator
from pymongo import IndexModel


class Event(Document):
    title: str = Field(max_length=255)
    description: str = Field(max_length=1000)
    banner_img_url: str | None = Field(default=None, max_length=500)
    date: date_type
    location: str = Field(max_length=255)
    capacity: int = Field(gt=0)
    sub_price: Decimal = Field(decimal_places=2, max_digits=10)

    @field_validator("sub_price", mode="before")
    @classmethod
    def normalize_sub_price(cls, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value

    class Settings:
        name = "events"
        indexes = [
            IndexModel([("title", 1)], unique=True),
            IndexModel([("description", 1)], unique=True),
            IndexModel([("date", 1), ("location", 1)], unique=True),
        ]
