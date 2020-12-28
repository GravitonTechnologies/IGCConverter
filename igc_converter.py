import os
from igcparser import IGCParser
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


class IGCConverter:
    def __init__(self, igc_input: str, output_format):
        self.igc_input = igc_input
        self.output_format = output_format
        self._convert_igc()

    def _convert_igc(self):
        if os.path.isdir(self.igc_input):
            igc_files = get_igc_files(self.igc_input)
            if len(igc_files) == 0:
                raise RuntimeError("No IGC files found in directory '{}'".format(self.igc_input))

            for igc_file in igc_files:
                self._do_conversion(igc_file)

        else:
            self._do_conversion(self.igc_input)

    def _do_conversion(self, igc_file_path: str):
        igc_parser = IGCParser(igc_file_path)
        destination_path = make_export_path(igc_file_path, self.output_format)
        exporter = FlightInfoExporterFactory().create(destination_path)
        exporter.export(igc_parser.flight_info, destination_path)
