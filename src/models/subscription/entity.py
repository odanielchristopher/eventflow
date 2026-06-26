from datetime import date as date_type
from decimal import Decimal

from beanie import Document
from pydantic import Field
from pymongo import IndexModel

from src.models.checkin.entity import CheckIn


class Subscription(Document):
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    price: Decimal = Field(decimal_places=2, max_digits=10)
    registered_at: date_type = Field(default_factory=date_type.today)
    event_id: str
    check_in: CheckIn | None = None

    class Settings:
        name = "subscriptions"
        indexes = [
            IndexModel([("email", 1), ("event_id", 1)], unique=True),
            IndexModel([("event_id", 1), ("registered_at", -1)]),
            IndexModel([("name", 1)]),
        ]
