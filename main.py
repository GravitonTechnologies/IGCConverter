from parser import IGCParser
from exporter_factory import FlightInfoExporterFactory


def main():
    parser = IGCParser('06ed9wl1.igc')
    destination_path = '06ed9wl1.csv'
    exporter = FlightInfoExporterFactory().create(destination_path)
    exporter.export(parser.flight_info, destination_path)


if __name__ == '__main__':
    main()
