from flight import FlightInfo, TimedFlightData, DifferentialGPS, KSection, JSection
import re
import datetime


class ParseError(Exception):
    def __init__(self, message, line_number: int, igc_file_path: str):
        super().__init__(message)
        self.line_number = line_number
        self.igc_file_path = igc_file_path
        self.message = message

    def __str__(self):
        return "Parse error: {} in '{}' at line {}.".format(self.message, self.igc_file_path, self.line_number)


class IGCParser:
    def __init__(self, igc_file_path=None):
        self.found_extension_header = False
        self.found_j_section = False
        self.current_line_number = 0
        self.igc_file_path = igc_file_path
        self.indices_to_extension_header_title = {}  # tuple of indices to title
        self.flight_info = FlightInfo()  # Empty flight info
        if igc_file_path is not None:
            # extract IGC file lines into list
            self.igc_file_lines = list(open(igc_file_path, 'r').readlines())
            self._parse_igc_lines()

    def _raise_parse_error(self, message):
        raise ParseError(message, self.current_line_number, self.igc_file_path)

    def _parse_igc_lines(self):
        self.current_line_number = 1
        for line in self.igc_file_lines:
            line = line.rstrip('\n')
            if line.startswith('H'):
                self._parse_header(line)
            elif line.startswith('A'):
                self._parse_flight_recorder_info(line)
            elif line.startswith('I'):
                self._parse_extension_header(line)
            elif line.startswith('B'):
                self._parse_timed_flight_data(line)
            elif line.startswith('L'):
                self._parse_comment_section(line)
            elif line.startswith('D'):
                self._parse_differential_gps(line)
            elif line.startswith('J'):
                self._parse_j_section(line)
            elif line.startswith('K'):
                self._parse_k_section(line)
            self.current_line_number += 1

    def _parse_j_section(self, line):
        self.found_j_section = True
        self.flight_info.j_section = JSection()

        line = line.removeprefix('J')
        num_extensions = -1
        try:
            num_extensions = int(line[0:2])
        except ValueError:
            self._raise_parse_error('unable to get extension parts from {}'.format(line))

        assert num_extensions >= 0
        self.flight_info.j_section.num_extensions = num_extensions

        line = line[2:]  # remove num extensions
        extensions = re.findall(r'(\d{4}[A-Z]{3})', line)
        for extension in extensions:
            extension_parts = re.search(r'(\d{2})(\d{2})([A-Z]{3})', extension)
            if extension_parts:
                start_index = int(
                    extension_parts.group(1))  # compensate for offset in IGC standard relative to python
                end_index = int(extension_parts.group(2)) + 1
                name = extension_parts.group(3)
                self.flight_info.j_section.flight_data_indices[name] = (start_index, end_index)
            else:
                self._raise_parse_error('unable to get extension parts from {}'.format(line))

    def _parse_k_section(self, line):
        if not self.found_j_section:
            self._raise_parse_error("invalid IGC file")

        k_section = KSection()

        k_section.utc_timestamp = line[1:7]
        for (title, indices) in self.flight_info.j_section.flight_data_indices.items():
            k_section.flight_data_values[title] = line[indices[0] - 1:indices[1]]

        self.flight_info.k_sections.append(k_section)

    def _parse_differential_gps(self, line):
        self.flight_info.differential_gps = DifferentialGPS()
        self.flight_info.differential_gps.gps_qualifier = line[1]
        if line[1] == '2':
            self.flight_info.differential_gps.dgps_station_id = line[1:]

    def _parse_comment_section(self, line):
        line = line.removeprefix('L')
        self.flight_info.comments.add(line)

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
            data.extension_values = {}
            for (title, indices) in self.flight_info.extension_header.extended_data_indices.items():
                data.extension_values[title] = line[indices[0] - 1:indices[1]]

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
                self.flight_info.extension_header.extended_data_indices[name] = (start_index, end_index)

            else:
                self._raise_parse_error('Extension Header parse error: {}'.format(line))

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
        elif line.startswith('HFTZN'):
            self._parse_timezone(line)

    def _parse_timezone(self, line):
        try:
            self.flight_info.header.time_zone = float(line.split(':')[1])
        except IndexError:
            self.flight_info.header.time_zone = float(line.split()[1])
        except ValueError:
            self._raise_parse_error('invalid timezone in {}'.format(line))

    def _parse_firmware_version(self, line):
        try:
            self.flight_info.header.firmware_version = line.split(':')[1]
        except IndexError:
            self._raise_parse_error('Parse Error: firmware version from {}'.format(line))

    def _parse_hardware_version(self, line):
        try:
            self.flight_info.header.hardware_version = line.split(':')[1]
        except IndexError:
            self._raise_parse_error('unable to get hardware version from {}'.format(line))

    def _parse_flight_recorder_type(self, line):
        try:
            self.flight_info.header.flight_recorder_type = line.split(':')[1]
        except IndexError:
            self._raise_parse_error('unable to get flight_recorder_type from {}'.format(line))

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
            self._raise_parse_error('unable to get gps datum from {}'.format(line))

        try:
            self.flight_info.header.gps_datum_num = line[5:8]
        except IndexError:
            self._raise_parse_error('unable to get gps datum num from {}'.format(line))

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
            self._raise_parse_error('unable to parse flight_recorder_manufacturer_code in {}'.format(line))

        try:
            self.flight_info.flight_recorder_info.flight_recorder_serial_number = line[4:7]
        except IndexError:
            self._raise_parse_error('unable to parse flight_recorder_serial_number in {}'.format(line))

        try:
            self.flight_info.flight_recorder_info.daily_flight_number = line.split(':')[1]
        except IndexError:
            self.flight_info.flight_recorder_info.daily_flight_number = line
            # self._raise_parse_error('unable to parse daily_flight_number in {}'.format(line))

    def _parse_pilot_info(self, line: str):
        self.flight_info.header.is_pilot_in_charge = 'PILOTINCHARGE' in line
        try:
            self.flight_info.header.pilot_name = line.split(':')[1]
        except IndexError:
            self.flight_info.header.pilot_name = ''
