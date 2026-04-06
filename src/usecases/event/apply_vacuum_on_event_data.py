from src.core import delta_lake_cli

class ApplyVaccumOnEventDataUseCase:
  @staticmethod
  def execute():
    delta_lake_cli.events.vacuum()