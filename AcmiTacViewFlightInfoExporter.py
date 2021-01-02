from exporter import FlightInfoExporter
from flight import FlightInfo
from typing import Optional
import datetime
import re
import collections


class AcmiTacViewFlightInfoExporter(FlightInfoExporter):
    def __init__(self):
        self.flight_info: Optional[FlightInfo] = None
        self._acmi_file = None
        self._reference_date = None
        self._aircraft_object_id = '1'
        self._longitude_format_regex = r"(\d{3})(\d{2})(\d{3})([EW])"
        self._latitude_format_regex = r"(\d{2})(\d{2})(\d{3})([NS])"
        self._float_format = '%.7f'

    def export(self, flight_info: FlightInfo, destination_path: str):
        self.flight_info = flight_info
        self._acmi_file = open(destination_path, 'w')

        self._export_header()
        self._export_reference_time()
        self._export_timed_flight_data()

        self._acmi_file.close()

    def _write_file_line(self, line: str):
        if not line.endswith('\n'):
            line = line + '\n'
        self._acmi_file.write(line)

    def _export_header(self):
        self._write_file_line('FileType=text/acmi/tacview')
        self._write_file_line('FileVersion=2.1')

    def _transform_longitude_format(self, longitude: str) -> str:
        result = re.search(self._longitude_format_regex, longitude)
        if result:
            degrees = result.group(1)
            minutes = result.group(2)
            decimals = result.group(3)
            direction = result.group(4)
        else:
            raise RuntimeError('unable to parse longitude')

        value = int(degrees) + (float(minutes + '.' + decimals) / 60)
        if direction.upper() == 'W':
            value *= -1
        return self._float_format % value

    def _transform_latitude_format(self, latitude: str) -> str:
        result = re.search(self._latitude_format_regex, latitude)
        if result:
            degrees = result.group(1)
            minutes = result.group(2)
            decimals = result.group(3)
            direction = result.group(4)
        else:
            raise RuntimeError('unable to parse longitude')
        value = int(degrees) + (float(minutes + '.' + decimals) / 60)
        if direction.upper() == 'S':
            value *= -1
        return self._float_format % value

    def _export_timed_flight_data(self):
        for timed_data in self.flight_info.timed_flight_data:
            r = self._get_reference_year_mon_day_hour_min_sec()

            current_date = datetime.datetime(int(r.year), int(r.month), int(r.day),
                                             int(r.hour), int(r.minute), int(r.second))

            self._write_file_line('#' + str((current_date - self._reference_date).seconds))

            additional_info = '|'.join([self._transform_longitude_format(timed_data.longitude),
                                        self._transform_latitude_format(timed_data.latitude), timed_data.gps_altitude])

            self._write_file_line(self._aircraft_object_id + ',' + additional_info)

    def _get_reference_year_mon_day_hour_min_sec(self) -> collections.namedtuple:
        ReferenceDateTime = collections.namedtuple('ReferenceDateTime',
                                                   ['year', 'month', 'day', 'hour', 'minute', 'second'])

        reference_year = '20' + str(self.flight_info.header.flight_date[0])  # assume 21st century
        reference_month = str(self.flight_info.header.flight_date[1])
        reference_day = str(self.flight_info.header.flight_date[2])
        reference_hour = self.flight_info.timed_flight_data[0].utc_time[0:2]
        reference_min = self.flight_info.timed_flight_data[0].utc_time[2:4]
        reference_sec = self.flight_info.timed_flight_data[0].utc_time[4:6]

        return ReferenceDateTime(year=reference_year, month=reference_month, day=reference_day, hour=reference_hour,
                                 minute=reference_min, second=reference_sec)

    def _export_reference_time(self):
        r = self._get_reference_year_mon_day_hour_min_sec()

        self._reference_date = datetime.datetime(int(r.year), int(r.month), int(r.day),
                                                 int(r.hour), int(r.minute), int(r.second))

        s = '0,ReferenceTime={}-{}-{}T{}:{}:{}Z'.format(r.year, r.month, r.day, r.hour,
                                                        r.minute, r.second)

        self._write_file_line(s)
