from src.core import delta_lake_cli
from src.models import Event, PaginatedData

class ListAllEventsUseCase:
  @staticmethod
  def execute(page: int = 1, per_page: int = 12) -> PaginatedData[Event]:
    limit = max(per_page, 1)
    offset = (max(page, 1) - 1) * limit

    data = delta_lake_cli.events.find_many(limit=limit, offset=offset)

    total = delta_lake_cli.events.count()

    return {
      "data": data,
      "meta": { "total": total, "page": page, "per_page": per_page }
    }
