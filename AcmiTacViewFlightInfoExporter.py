from exporter import FlightInfoExporter
from flight import FlightInfo
from typing import Optional
import datetime


class AcmiTacViewFlightInfoExporter(FlightInfoExporter):
    def __init__(self):
        self.flight_info: Optional[FlightInfo] = None
        self._acmi_file = None

    def export(self, flight_info: FlightInfo, destination_path: str):
        self.flight_info = flight_info
        self._acmi_file = open(destination_path, 'w')

        self._export_header()
        self._export_reference_time()

        self._acmi_file.close()

    def _write_file_line(self, line: str):
        if not line.endswith('\n'):
            line = line + '\n'
        self._acmi_file.write(line)

    def _export_header(self):
        self._write_file_line('FileType=text/acmi/tacview')
        self._write_file_line('FileVersion=2.1')

    def _export_reference_time(self):
        reference_year = '20' + str(self.flight_info.header.flight_date[0])  # assume 21st century
        reference_month = str(self.flight_info.header.flight_date[1])
        reference_day = str(self.flight_info.header.flight_date[2])
        reference_hour = self.flight_info.timed_flight_data[0].utc_time[0:2]
        reference_min = self.flight_info.timed_flight_data[0].utc_time[2:4]
        reference_sec = self.flight_info.timed_flight_data[0].utc_time[4:6]

        s = '0,ReferenceTime={}-{}-{}T{}:{}:{}Z'.format(reference_year, reference_month, reference_day, reference_hour,
                                                        reference_min, reference_sec)
        self._write_file_line(s)
