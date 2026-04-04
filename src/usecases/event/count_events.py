from src.core import delta_lake_cli


class CountEventsUseCase:
  @staticmethod
  def execute() -> int:
    return delta_lake_cli.events.count()
