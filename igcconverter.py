import os
from igcparser import IGCParser, ParseError
from exporterfactory import FlightInfoExporterFactory
import abc
from typing import List


def get_igc_files(directory: str) -> List[str]:
    igc_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".igc"):
            igc_files.append(directory + os.sep + filename)
    return igc_files


def make_export_path(in_path: str, export_format: str):
    if not export_format.startswith('.'):
        export_format = '.' + export_format

    return os.path.splitext(in_path)[0] + export_format


class ConversionProgressObserver:
    @abc.abstractmethod
    def on_conversion_started(self, num_items: int):
        raise NotImplemented

    @abc.abstractmethod
    def on_conversion_completed(self):
        raise NotImplemented

    @abc.abstractmethod
    def on_file_converted(self):
        raise NotImplemented


class IGCConverterExceptionObserver:
    @abc.abstractmethod
    def on_exception_raised(self, e: Exception):
        raise NotImplemented


class IGCConverter:
    def __init__(self, igc_input: str, output_format):
        self.igc_input = igc_input
        self.output_format = output_format
        self._progress_observers: List[ConversionProgressObserver] = []
        self._exception_observers: List[IGCConverterExceptionObserver] = []

    def add_progress_observer(self, o: ConversionProgressObserver):
        self._progress_observers.append(o)

    def add_exception_observer(self, o: IGCConverterExceptionObserver):
        self._exception_observers.append(o)

    def _notify_observers_conversion_started(self, num_items: int):
        for o in self._progress_observers:
            o.on_conversion_started(num_items)

    def _notify_observers_file_converted(self):
        for o in self._progress_observers:
            o.on_file_converted()

    def _notify_observers_conversion_completed(self):
        for o in self._progress_observers:
            o.on_conversion_completed()

    def _notify_observers_exception_raised(self, e: Exception):
        for o in self._exception_observers:
            o.on_exception_raised(e)

    def convert_igc(self):
        if os.path.isdir(self.igc_input):
            igc_files = get_igc_files(self.igc_input)
        else:
            igc_files = [self.igc_input]

        if len(igc_files) == 0:
            self._notify_observers_exception_raised(
                RuntimeError("No IGC files found in directory '{}'".format(self.igc_input)))

        self._notify_observers_conversion_started(len(igc_files))
        for igc_file in igc_files:
            try:
                self._do_conversion(igc_file)
            except Exception as e:
                self._notify_observers_exception_raised(e)
            else:
                self._notify_observers_file_converted()
        self._notify_observers_conversion_completed()

    def _do_conversion(self, igc_file_path: str):
        igc_parser = IGCParser(igc_file_path)
        destination_path = make_export_path(igc_file_path, self.output_format)
        exporter = FlightInfoExporterFactory().create(destination_path)
        exporter.export(igc_parser.flight_info, destination_path)
