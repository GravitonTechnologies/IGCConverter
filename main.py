from parser import IGCParser
from exporter_factory import FlightInfoExporterFactory
import os


def get_igc_files(directory: str):
    igc_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".igc"):
            igc_files.append(filename)
    return igc_files


def make_export_path(in_path: str, export_format: str):
    if not export_format.startswith('.'):
        export_format = '.' + export_format

    return os.path.splitext(in_path)[0] + export_format


def main():
    csv_file_path = '06ed9wl1.igc'
    parser = IGCParser(csv_file_path)
    destination_path = make_export_path(csv_file_path, 'csv')
    exporter = FlightInfoExporterFactory().create(destination_path)
    exporter.export(parser.flight_info, destination_path)


if __name__ == '__main__':
    main()
