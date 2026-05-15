from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.db import get_session
from src.infra.repositories.event_repository import SqlModelEventRepository


def get_event_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlModelEventRepository:
    return SqlModelEventRepository(session)
