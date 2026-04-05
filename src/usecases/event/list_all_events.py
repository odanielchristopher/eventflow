from src.core import delta_lake_cli
from src.models import Event

class ListAllEventsUseCase:
  @staticmethod
  def execute(page: int = 1, per_page: int = 12) -> list[Event]:
    limit = max(per_page, 1)
    offset = (max(page, 1) - 1) * limit

    return delta_lake_cli.events.find_many(limit=limit, offset=offset)
