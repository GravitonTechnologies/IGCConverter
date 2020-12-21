from parser import IGCParser
from exporter_factory import FlightInfoExporterFactory
import os


def get_igc_files(directory: str):
    igc_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".igc"):
            igc_files.append(filename)
    return igc_files

def main():
    parser = IGCParser('06ed9wl1.igc')
    destination_path = '06ed9wl1.csv'
    exporter = FlightInfoExporterFactory().create(destination_path)
    exporter.export(parser.flight_info, destination_path)


if __name__ == '__main__':
    main()
