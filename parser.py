from flight import FlightInfo, TimedFlightData
import re
import datetime


class IGCParser:
    def __init__(self, igc_file_path):
        self.found_extension_header = False
        self.flight_info = FlightInfo()  # Empty flight info

        # extract IGC file lines into list
        self.igc_file_lines = list(open(igc_file_path, 'r').readlines())
        self._parse_igc_lines()

    def _parse_igc_lines(self):
        for line in self.igc_file_lines:
            if line.startswith('H'):
                self._parse_header(line)
            elif line.startswith('A'):
                self._parse_flight_recorder_info(line)
            elif line.startswith('I'):
                self._parse_extension_header(line)
            elif line.startswith('B'):
                self._parse_timed_flight_data(line)

    def _parse_timed_flight_data(self, line):
        data = TimedFlightData()
        data.raw_data = line

        data.utc_time = line[1:7]
        data.latitude = line[7:15]
        data.longitude = line[15:24]
        data.fix_validity = line[24:25]
        data.pressure_altitude = line[25:30]
        data.gps_altitude = line[30:35]

        if self.found_extension_header:
            data.additional_data = self.flight_info.extension_header.flight_data

        self.flight_info.timed_flight_data.append(data)

    def _parse_extension_header(self, line):
        self.found_extension_header = True
        line = line.removeprefix('I')
        num_extensions = int(line[0:2])
        self.flight_info.extension_header.num_extensions = num_extensions

        line = line[2:]  # remove num extensions
        extensions = re.findall(r'(\d{4}[A-Z]{3})', line)
        for extension in extensions:
            extension_parts = re.search(r'(\d{2})(\d{2})([A-Z]{3})', extension)
            if extension_parts:
                start_index = int(extension_parts.group(1))
                end_index = int(extension_parts.group(2))
                name = extension_parts.group(3)
                self.flight_info.extension_header.flight_data[name] = (start_index, end_index)

            else:
                print('unable to get extension parts from {}'.format(line))

    def _parse_header(self, line):
        if line.startswith('HFPLT'):
            self._parse_pilot_info(line)
        elif line.startswith('HFDTE'):
            self._parse_flight_date(line)
        elif line.startswith('HFCM2CREW2'):
            self._parse_second_pilot_name(line)
        elif line.startswith('HFGTY'):
            self._parse_glider_type(line)
        elif line.startswith('HFGID'):
            self._parse_glider_id(line)
        elif line.startswith('HFDTM'):
            self._parse_gps_datum(line)
        elif line.startswith('HFRFW'):
            self._parse_firmware_version(line)
        elif line.startswith('HFRHW'):
            self._parse_hardware_version(line)
        elif line.startswith('HFFTY'):
            self._parse_flight_recorder_type(line)
        elif line.startswith('HFGPS'):
            self._parse_gps_info(line)
        elif line.startswith('HFPRS'):
            self._parse_pressure_sensor_info(line)
        elif line.startswith('HFCID'):
            self._parse_tail_fin_number(line)
        elif line.startswith('HFCCL'):
            self._parse_glider_class(line)

    def _parse_firmware_version(self, line):
        try:
            self.flight_info.header.firmware_version = line.split(':')[1]
        except IndexError:
            print('unable to get firmware version from {}'.format(line))

    def _parse_hardware_version(self, line):
        try:
            self.flight_info.header.hardware_version = line.split(':')[1]
        except IndexError:
            print('unable to get hardware version from {}'.format(line))

    def _parse_flight_recorder_type(self, line):
        try:
            self.flight_info.header.flight_recorder_type = line.split(':')[1]
        except IndexError:
            print('unable to get flight_recorder_type from {}'.format(line))

    def _parse_gps_info(self, line):
        info = line.removeprefix('HFGPS').removeprefix('RECEIVER:')
        assert 'HFGPS' not in info, "prefix wasn't removed!"
        self.flight_info.header.gps_info = info

    def _parse_pressure_sensor_info(self, line):
        info = line.removeprefix('HFPRS').removeprefix('PRESSALTSENSOR:')
        assert 'HFPRS' not in info, "prefix wasn't removed!"
        self.flight_info.header.pressure_sensor_info = info

    def _parse_tail_fin_number(self, line):
        try:
            self.flight_info.header.tail_fin_number = line.split(':')[1]
        except IndexError:
            pass

    def _parse_glider_class(self, line):
        try:
            self.flight_info.header.glider_class = line.split(':')[1]
        except IndexError:
            pass

    def _parse_gps_datum(self, line):
        try:
            self.flight_info.header.gps_datum = line.split(':')[1]
        except IndexError:
            print('unable to get gps datum from {}'.format(line))

        try:
            self.flight_info.header.gps_datum_num = int(line[5:8])
        except IndexError:
            print('unable to get gps datum num from {}'.format(line))
        except ValueError:
            print('invalid to get gps datum num from {}'.format(line))

    def _parse_glider_type(self, line):
        try:
            self.flight_info.header.glider_type = line.split(':')[1]
        except IndexError:
            pass

    def _parse_glider_id(self, line):
        try:
            self.flight_info.header.glider_id = line.split(':')[1]
        except IndexError:
            pass

    def _parse_second_pilot_name(self, line):
        try:
            self.flight_info.header.second_pilot_name = line.split(':')[1]
        except IndexError:
            pass

    def _parse_flight_date(self, line):
        date_search = re.search(r"(\d{2})(\d{2})(\d{2})", line)
        if date_search:
            str_day = date_search.group(1)
            str_month = date_search.group(2)
            str_year = date_search.group(3)  # todo: maybe append '19' or '20' to year
            self.flight_info.header.flight_date = datetime.date(int(str_year), int(str_month), int(str_day))

    def _parse_flight_recorder_info(self, line: str):
        try:
            self.flight_info.flight_recorder_info.flight_recorder_manufacturer_code = line[1:4]
        except IndexError:
            print('unable to parse flight_recorder_manufacturer_code in {}'.format(line))

        try:
            self.flight_info.flight_recorder_info.flight_recorder_serial_number = line[4:7]
        except IndexError:
            print('unable to parse flight_recorder_serial_number in {}'.format(line))

        try:
            self.flight_info.flight_recorder_info.daily_flight_number = line.split(':')[1]
        except IndexError:
            print('unable to parse daily_flight_number in {}'.format(line))

    def _parse_pilot_info(self, line: str):
        self.flight_info.header.is_pilot_in_charge = 'PILOTINCHARGE' in line
        try:
            self.flight_info.header.pilot_name = line.split(':')[1]
        except IndexError:
            self.flight_info.header.pilot_name = ''
