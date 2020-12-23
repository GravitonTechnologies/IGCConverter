import os
from parser import IGCParser
from exporter_factory import FlightInfoExporterFactory


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


def convert_igc(igc_input: str, output_format):
    if os.path.isdir(igc_input):
        igc_files = get_igc_files(igc_input)
        if len(igc_files) == 0:
            raise RuntimeError("No IGC files found in directory '{}'".format(igc_input))

        for igc_file in igc_files:
            igc_parser = IGCParser(igc_file)
            destination_path = make_export_path(igc_file, output_format)
            exporter = FlightInfoExporterFactory().create(destination_path)
            exporter.export(igc_parser.flight_info, destination_path)
    else:
        igc_parser = IGCParser(igc_input)
        destination_path = make_export_path(igc_input, output_format)
        exporter = FlightInfoExporterFactory().create(destination_path)
        exporter.export(igc_parser.flight_info, destination_path)
