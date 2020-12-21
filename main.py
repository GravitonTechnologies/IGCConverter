from parser import IGCParser
from exporter_factory import FlightInfoExporterFactory
import os
import argparse


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default='csv', type=str)
    parser.add_argument("input", default='csv', type=str)
    args = parser.parse_args()

    if os.path.isdir(args.input):
        igc_files = get_igc_files(args.input)
        for igc_file in igc_files:
            igc_parser = IGCParser(igc_file)
            destination_path = make_export_path(igc_file, args.format)
            exporter = FlightInfoExporterFactory().create(destination_path)
            exporter.export(igc_parser.flight_info, destination_path)
    else:
        igc_parser = IGCParser(args.input)
        destination_path = make_export_path(args.input, args.format)
        exporter = FlightInfoExporterFactory().create(destination_path)
        exporter.export(igc_parser.flight_info, destination_path)


if __name__ == '__main__':
    main()
