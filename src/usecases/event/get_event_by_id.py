from fastapi import HTTPException

from src.core import delta_lake_cli

class GetEventByIdUseCase:
  @staticmethod
  def execute(event_id: int):
    event = delta_lake_cli.events.get(event_id)

    if event is None:
      raise HTTPException(status_code=404, detail="Event not found")

    return event