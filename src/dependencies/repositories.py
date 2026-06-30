from __future__ import annotations

from src.infra.repositories.activity_repository import BeanieActivityRepository
from src.infra.repositories.document_repository import BeanieDocumentRepository
from src.infra.repositories.event_repository import BeanieEventRepository
from src.infra.repositories.speaker_repository import BeanieSpeakerRepository
from src.infra.repositories.subscription_repository import SqlModelSubscriptionRepository


def get_event_repository() -> BeanieEventRepository:
    return BeanieEventRepository()


def get_document_repository() -> BeanieDocumentRepository:
    return BeanieDocumentRepository()


def get_subscription_repository() -> SqlModelSubscriptionRepository:
    return SqlModelSubscriptionRepository()


def get_speaker_repository() -> BeanieSpeakerRepository:
    return BeanieSpeakerRepository()


def get_activity_repository() -> BeanieActivityRepository:
    return BeanieActivityRepository()
