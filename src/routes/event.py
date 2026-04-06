from __future__ import annotations

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from src.models import CreateEventDto, UpdateEventDto, Event, CountEventsResponse, ListEventsResponse

from src.usecases.event import CreateEventUseCase, ListAllEventsUseCase, ExportCsvUseCase, ExportCsvZipUseCase, UpdateEventUseCase, GetEventByIdUseCase, DeleteEventUseCase, CountEventsUseCase, ApplyVaccumOnEventDataUseCase

router = APIRouter(prefix="/events", tags=["events"])

@router.get('', response_model=ListEventsResponse)
def get_all_events(page: int = 1, per_page: int = 10):
    return ListAllEventsUseCase().execute(page, per_page)

@router.get('/count', response_model=CountEventsResponse)
def count_events():
    total = CountEventsUseCase().execute()

    return { "total": total }

@router.get('/vacuum', status_code=204, response_model=None)
def apply_vacuum():
    return ApplyVaccumOnEventDataUseCase().execute()

@router.post('', response_model=Event, status_code=201)
def create_event(create_event_dto: CreateEventDto):
    return CreateEventUseCase().execute(create_event_dto)

@router.get(
    "/csv",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {
                "text/csv": {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                    }
                }
            },
            "description": "CSV export stream",
        }
    },
)
def export_csv():
    return StreamingResponse(
        ExportCsvUseCase().execute(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=events.csv"
        }
    )

@router.get(
    "/csv/zip",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {
                "application/zip": {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                    }
                }
            },
            "description": "ZIP export stream",
        }
    },
)
def export_csv_zip():
    return StreamingResponse(
        ExportCsvZipUseCase().execute(),
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=events.zip"
        }
    )

@router.get('/{event_id}', response_model=Event)
def get_event_by_id(event_id: int):
    return GetEventByIdUseCase().execute(event_id)

@router.put('/{event_id}', response_model=Event)
def update_event(event_id: int, update_event_dto: UpdateEventDto):
    return UpdateEventUseCase().execute(event_id, update_event_dto)

@router.delete(
    '/{event_id}',
    status_code=204,
    response_model=None,
    responses={204: {"description": "Event deleted successfully"}},
)
def delete_event(event_id: int) -> Response:
    DeleteEventUseCase().execute(event_id)
    return Response(status_code=204)
