from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from src.models.activity_speaker.entity import ActivitySpeaker

if TYPE_CHECKING:
    from src.models.activity.entity import Activity


class Speaker(SQLModel, table=True):
    __tablename__ = "speakers"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(length=255), nullable=False))
    specialty: str = Field(sa_column=Column(String(length=255), nullable=False))
    bio: str = Field(sa_column=Column(String(length=1000), nullable=False))

    activities: list["Activity"] = Relationship(
        back_populates="speakers",
        link_model=ActivitySpeaker,
    )
