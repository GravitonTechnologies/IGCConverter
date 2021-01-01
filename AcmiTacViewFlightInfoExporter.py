from exporter import FlightInfoExporter
from flight import FlightInfo


class AcmiTacViewFlightInfoExporter(FlightInfoExporter):
    def export(self, flight_info: FlightInfo, destination_path: str):
        raise NotImplemented
