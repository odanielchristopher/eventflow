from __future__ import annotations

from fastapi import APIRouter
from typing import Literal
from fastapi.responses import StreamingResponse


from src.models import CreateEventDto

from src.usecases.event import CreateEventUseCase
from src.usecases.event import ListAllEventsUseCase
from src.usecases.event import ExportCsvUseCase

router = APIRouter(prefix="/events", tags=["events"])

@router.get('')
def get_all_events(page: int = 1, per_page: int = 10):
    return ListAllEventsUseCase().execute(page, per_page)

@router.post('')
def create_event(createEventDto: CreateEventDto):
    return CreateEventUseCase().execute(createEventDto)

@router.get("/csv")
def export_csv():
    return StreamingResponse(
        ExportCsvUseCase().execute(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=events.csv"
        }
    )