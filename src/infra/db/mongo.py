from __future__ import annotations

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import get_settings
from src.models.event import EventEntity
from src.models.subscription import Subscription

settings = get_settings()

mongo_client: AsyncIOMotorClient | None = None


async def init_mongo() -> None:
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(
        database=mongo_client[settings.mongodb_database],
        document_models=[EventEntity, Subscription],
    )


def close_mongo() -> None:
    if mongo_client is not None:
        mongo_client.close()
