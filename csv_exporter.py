from exporter import FlightInfoExporter, FlightInfo
import csv
from typing import Optional


class CSVFlightInfoExporter(FlightInfoExporter):
    def __init__(self):
        self.flight_info: Optional[FlightInfo] = None
        self.flight_data = {}  # timestamp to data list
        self.titles = ['UTC Time', 'Longitude', 'Latitude', 'GPS Alt', 'Fix Validity', 'Pressure Altitude']
        self.values = []
        self.writer = None

    def _add_additional_titles(self):
        # add additional titles from I record
        for timed_flight_data in self.flight_info.timed_flight_data:
            additional_titles = timed_flight_data.extension_values.keys()
            for t in additional_titles:
                if t not in self.titles:
                    self.titles.append(t)

    def _export_flight_data(self):
        # Add values to table
        for timed_flight_data in self.flight_info.timed_flight_data:
            # standard values
            values = [timed_flight_data.utc_time, timed_flight_data.longitude, timed_flight_data.latitude,
                      timed_flight_data.gps_altitude,
                      timed_flight_data.fix_validity, timed_flight_data.pressure_altitude]

            self.flight_data[timed_flight_data.utc_time] = values

            # optional values
            if timed_flight_data.extension_values is not None:
                for (title, value) in timed_flight_data.extension_values.items():
                    index = self.titles.index(title)
                    values.insert(index, value)

            self.values.append(values)

    def _export_j_and_k_sections(self):
        if self.flight_info.j_section is None:
            return

        # TODO: Make sure value is always aligned with table title
        # Add values to table

        for k_section in self.flight_info.k_sections:
            utc_time = k_section.utc_timestamp

            for (title, value) in k_section.flight_data_values.items():
                if title not in self.titles:
                    self.titles.append(title)
                self.flight_data[utc_time].append(value)

    def export(self, flight_info: FlightInfo, destination_path: str):
        self.flight_info = flight_info
        with open(destination_path, 'w', newline='') as csvfile:
            self.writer = csv.writer(csvfile)
            self._add_additional_titles()
            self._export_flight_data()
            self._export_j_and_k_sections()

            self.writer.writerow(self.titles)
            self.writer.writerows(self.values)
