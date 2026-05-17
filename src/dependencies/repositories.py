from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.db import get_session
from src.infra.repositories.activity_repository import SqlModelActivityRepository
from src.infra.repositories.document_repository import SqlModelDocumentRepository
from src.infra.repositories.event_repository import SqlModelEventRepository
from src.infra.repositories.speaker_repository import SqlModelSpeakerRepository
from src.infra.repositories.subscription_repository import SqlModelSubscriptionRepository


def get_event_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlModelEventRepository:
    return SqlModelEventRepository(session)


def get_document_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlModelDocumentRepository:
    return SqlModelDocumentRepository(session)


def get_subscription_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlModelSubscriptionRepository:
    return SqlModelSubscriptionRepository(session)


def get_speaker_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlModelSpeakerRepository:
    return SqlModelSpeakerRepository(session)


def get_activity_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlModelActivityRepository:
    return SqlModelActivityRepository(session)
