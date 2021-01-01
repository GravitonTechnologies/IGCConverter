from exporter import FlightInfoExporter
from flight import FlightInfo
from typing import Optional


class AcmiTacViewFlightInfoExporter(FlightInfoExporter):
    def __init__(self):
        self.flight_info: Optional[FlightInfo] = None
        self._acmi_file = None

    def export(self, flight_info: FlightInfo, destination_path: str):
        self.flight_info = flight_info
        self._acmi_file = open(destination_path, 'w')

        self._export_header()

        self._acmi_file.close()

    def _write_file_line(self, line: str):
        if not line.endswith('\n'):
            line = line + '\n'
        self._acmi_file.write(line)

    def _export_header(self):
        self._write_file_line('FileType=text/acmi/tacview')
        self._write_file_line('FileVersion=2.1')
