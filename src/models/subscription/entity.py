from bson.decimal128 import Decimal128
from datetime import date as date_type
from decimal import Decimal

from beanie import Document
from pydantic import Field, field_validator
from pymongo import IndexModel

from src.models.checkin.entity import CheckIn


class Subscription(Document):
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    price: Decimal = Field(decimal_places=2, max_digits=10)
    registered_at: date_type = Field(default_factory=date_type.today)
    event_id: str
    check_in: CheckIn | None = None

    @field_validator("price", mode="before")
    @classmethod
    def normalize_price(cls, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value

    class Settings:
        name = "subscriptions"
        indexes = [
            IndexModel([("email", 1), ("event_id", 1)], unique=True),
            IndexModel([("event_id", 1), ("registered_at", -1)]),
            IndexModel([("name", 1)]),
        ]
