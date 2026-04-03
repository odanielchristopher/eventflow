from typing import Literal
from src.core import delta_lake_cli

class ListAllEventsUseCase:
  @staticmethod
  def execute(page = 1, per_page = 12):
    return delta_lake_cli.events.list(page=page, page_size=per_page)
