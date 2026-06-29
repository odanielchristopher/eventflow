from datetime import datetime, timezone

from beanie import Document as BeanieDocument
from pydantic import Field
from pymongo import IndexModel

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Document(BeanieDocument):
    original_filename: str = Field(max_length=255)
    content_type: str = Field(max_length=255)
    extension: str = Field(max_length=20)
    size_bytes: int = Field(ge=0)
    event_id: str | None = None
    created_at: datetime = Field(default_factory=utc_now)

    class Settings:
        name = "documents"
        indexes = [
            IndexModel([("event_id", 1), ("created_at", -1)]),
            IndexModel([("content_type", 1)]),
        ]
