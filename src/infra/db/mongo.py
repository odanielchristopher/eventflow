from __future__ import annotations

from beanie import init_beanie
from pymongo import AsyncMongoClient

from src.core.config import get_settings
from src.models.event import EventEntity
from src.models.speaker import Speaker
from src.models.subscription import Subscription

settings = get_settings()

mongo_client: AsyncMongoClient | None = None


async def init_mongo() -> None:
    global mongo_client
    mongo_client = AsyncMongoClient(settings.mongodb_url)
    await init_beanie(
        database=mongo_client[settings.mongodb_database],
        document_models=[EventEntity, Speaker, Subscription],
    )


async def close_mongo() -> None:
    if mongo_client is not None:
        await mongo_client.close()
