from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db import db_client, get_async_session
from src.infra.db.client import DatabaseClient


def get_db_client() -> DatabaseClient:
    return db_client


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_async_session():
        yield session
