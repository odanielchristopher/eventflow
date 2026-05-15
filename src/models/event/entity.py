from datetime import date as date_type
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, Numeric, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.document.entity import Document


class Event(SQLModel, table=True):
    __tablename__ = "events"
    __table_args__ = (
        UniqueConstraint("title", name="uq_events_title"),
        UniqueConstraint("description", name="uq_events_description"),
        UniqueConstraint("date", "location", name="uq_events_date_location"),
    )

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
    documents: list["Document"] = Relationship(back_populates="event")
