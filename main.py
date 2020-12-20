from parser import IGCParser
from exporter_factory import FlightInfoExporterFactory


def main():
    parser = IGCParser('test.igc')
    destination_path = 'test.csv'
    exporter = FlightInfoExporterFactory().create(destination_path)
    exporter.export(parser.flight_info, destination_path)


if __name__ == '__main__':
    main()
