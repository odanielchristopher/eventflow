from src.models import CreateEventDto
from src.core import delta_lake_cli

class CreateEventUseCase:
  @staticmethod
  def execute(event: CreateEventDto):
    return delta_lake_cli.events.create(event)
