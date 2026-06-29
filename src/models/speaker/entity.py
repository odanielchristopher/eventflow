from beanie import Document
from pydantic import Field
from pymongo import IndexModel


class Speaker(Document):
    name: str = Field(max_length=255)
    specialty: str = Field(max_length=255)
    bio: str = Field(max_length=1000)

    class Settings:
        name = "speakers"
        indexes = [
            IndexModel([("name", 1)]),
            IndexModel([("specialty", 1)]),
        ]
