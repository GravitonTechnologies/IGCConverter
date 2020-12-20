import abc
from flight import FlightInfo


class FlightInfoExporter:

    @abc.abstractmethod
    def export(self, flight_info: FlightInfo, destination_path: str):
        pass
