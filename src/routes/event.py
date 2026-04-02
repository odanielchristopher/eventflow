from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "resource": "events"}
