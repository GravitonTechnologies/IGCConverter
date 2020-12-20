from exporter import FlightInfoExporter
from csv_exporter import CSVFlightInfoExporter
import os.path


class FlightInfoExporterFactory:
    def __init__(self):
        self.exporters = {'csv': CSVFlightInfoExporter}

    def create(self, destination_path: str) -> FlightInfoExporter:
        extension = os.path.splitext(destination_path)[1].removeprefix('.')
        try:
            return self.exporters[extension]()
        except KeyError:
            print('Unsupported extension: ' + extension)
            exit(0)
