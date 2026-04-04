import csv
import io
from src.core import delta_lake_cli

class ExportCsvUseCase:

    @staticmethod
    def execute():
        repo = delta_lake_cli.event

        first_line = True
        fieldnames = None

        for batch in repo.export_batches(batch_size=100):
            if not batch:
                continue

            if fieldnames is None:
                fieldnames = list(batch[0].keys())

            output = io.StringIO(newline="")
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            if first_line:
                writer.writeheader()
                first_line = False

            writer.writerows(batch)

            output.seek(0)
            yield output.getvalue().encode("utf-8")