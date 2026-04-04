from __future__ import annotations

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from src.models import CreateEventDto, UpdateEventDto

from src.usecases.event import CreateEventUseCase, ListAllEventsUseCase, ExportCsvUseCase, ExportCsvZipUseCase, UpdateEventUseCase, GetEventByIdUseCase, DeleteEventUseCase

router = APIRouter(prefix="/events", tags=["events"])

@router.get('')
def get_all_events(page: int = 1, per_page: int = 10):
    return ListAllEventsUseCase().execute(page, per_page)

@router.get('/{event_id}')
def get_all_events(event_id: int):
    return GetEventByIdUseCase().execute(event_id)

@router.post('')
def create_event(create_event_dto: CreateEventDto):
    return CreateEventUseCase().execute(create_event_dto)

@router.put('/{event_id}')
def update_event(event_id: int, update_event_dto: UpdateEventDto):
    return UpdateEventUseCase().execute(event_id, update_event_dto)

@router.delete('/{event_id}', status_code=204)
def delete_event(event_id: int):
    DeleteEventUseCase().execute(event_id)
    return Response(status_code=204)

@router.get("/csv")
def export_csv():
    return StreamingResponse(
        ExportCsvUseCase().execute(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=events.csv"
        }
    )

@router.get("/csv/zip")
def export_csv_zip():
    return StreamingResponse(
        ExportCsvZipUseCase().execute(),
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=events.zip"
        }
    )
