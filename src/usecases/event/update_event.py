from fastapi import HTTPException

from src.models import UpdateEventDto, Event
from src.core import delta_lake_cli

class UpdateEventUseCase:
  @staticmethod
  def execute(event_id: int, update_dto: UpdateEventDto):
    event = delta_lake_cli.events.get(event_id)

    if event is None:
      raise HTTPException(status_code=404, detail="Event not found")
    
    updated_event = Event(
      id=event_id,
      **update_dto.model_dump()
    )

    return delta_lake_cli.events.update(event_id, updated_event)
