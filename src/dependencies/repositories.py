from __future__ import annotations

from src.infra.repositories.activity_repository import SqlModelActivityRepository
from src.infra.repositories.checkin_repository import SqlModelCheckInRepository
from src.infra.repositories.document_repository import SqlModelDocumentRepository
from src.infra.repositories.event_repository import SqlModelEventRepository
from src.infra.repositories.speaker_repository import SqlModelSpeakerRepository
from src.infra.repositories.subscription_repository import SqlModelSubscriptionRepository


def get_event_repository() -> SqlModelEventRepository:
    return SqlModelEventRepository()


def get_document_repository() -> SqlModelDocumentRepository:
    return SqlModelDocumentRepository(None)


def get_subscription_repository() -> SqlModelSubscriptionRepository:
    return SqlModelSubscriptionRepository()


def get_speaker_repository() -> SqlModelSpeakerRepository:
    return SqlModelSpeakerRepository(None)


def get_activity_repository() -> SqlModelActivityRepository:
    return SqlModelActivityRepository(None)


def get_check_in_repository() -> SqlModelCheckInRepository:
    return SqlModelCheckInRepository(None)
