from __future__ import annotations

from fastapi import APIRouter

from src.models.event import Event
from src.core.client import DeltaLakeClient

router = APIRouter(prefix="/events", tags=["events"])
client = DeltaLakeClient()

@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "resource": "events"}

@router.get('')
def get_all_events(page: int = 1, per_page: int = 10, order: str = 'asc'):
    return client.events.list(page=page,page_size=per_page, order_by=[("id", order)])

@router.post('')
def create_event(event: Event):
    return client.events.insert(event)