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

    def _export_flight_data(self):
        # Add titles to table
        for info_data in self.flight_info.timed_flight_data:
            if info_data.additional_data is not None:
                for title in info_data.additional_data.keys():
                    if title not in self.titles:
                        self.titles.append(title)

        # TODO: Make sure value is always aligned with table title
        # Add values to table
        for info_data in self.flight_info.timed_flight_data:
            # standard values
            values = [info_data.utc_time, info_data.longitude, info_data.latitude, info_data.gps_altitude,
                      info_data.fix_validity, info_data.pressure_altitude]

            self.flight_data[info_data.utc_time] = values

            # optional values
            if info_data.additional_data is not None:
                for indices in info_data.additional_data.values():
                    value = info_data.raw_data[indices[0]:indices[1]+1]
                    values.append(value)

            self.values.append(values)

    def _export_j_and_k_sections(self):
        if self.flight_info.j_section is None:
            return

        # TODO: Make sure value is always aligned with table title
        # Add values to table
        indices = self.flight_info.j_section.flight_data.values()

        for k_section in self.flight_info.k_sections:
            utc_time = k_section.raw_section_data[1:7]

            raw_data = k_section.raw_section_data
            for (title, indices) in k_section.flight_data.items():
                if title not in self.titles:
                    self.titles.append(title)
                self.flight_data[utc_time].append(raw_data[indices[0]: indices[1]])

    def export(self, flight_info: FlightInfo, destination_path: str):
        self.flight_info = flight_info
        with open(destination_path, 'w', newline='') as csvfile:
            self.writer = csv.writer(csvfile)
            self._export_flight_data()
            self._export_j_and_k_sections()

            self.writer.writerow(self.titles)
            self.writer.writerows(self.values)
