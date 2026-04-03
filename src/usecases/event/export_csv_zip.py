import zipstream 
from . import ExportCsvUseCase


class ExportCsvZipUseCase:

    @staticmethod
    def execute():
        zip = zipstream.ZipStream(compress_type=zipstream.ZIP_DEFLATED)

        zip.add(data=ExportCsvUseCase.execute(), arcname="events.csv")

        return zip