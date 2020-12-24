import datetime
from typing import Optional, Dict, Tuple, List


# K section of IGC file (infrequent timed data)
class KSection:
    def __init__(self):
        self.raw_section_data: str = ''
        self.flight_data: Dict[str, Tuple[int, int]] = {}  # maps name to tuple(start, end)

    def __str__(self):
        return ''


# J section of IGC file
class JSection:
    def __init__(self):
        self.num_extensions: int = 0
        self.flight_data: Dict[str, Tuple[int, int]] = {}  # maps name to tuple(start, end)

    def __str__(self):
        return 'num extensions: ' + str(self.num_extensions) + ', ' + str(self.flight_data)


class GPSInfo:
    def __init__(self):
        self.info: str = ''

    def __str__(self):
        return self.info


class PressureSensorInfo:
    def __init__(self):
        self.info: str = ''

    def __str__(self):
        return self.info


# I section of IGC file (defines what is appended to the timed data on B lines)
class ExtensionHeader:
    def __init__(self):
        self.num_extensions: int = 0
        self.extended_data_indices: Dict[str, Tuple[int, int]] = {}  # maps name to tuple(start, end)

    def __str__(self):
        res = 'num_extensions: ' + str(self.num_extensions) + '\n'
        return res


# B section of IGC file
class TimedFlightData:
    def __init__(self):
        self.extension_values: Optional[Dict[str, str]] = None  # Information from I section
        self.utc_time: str = ''
        self.latitude: str = ''
        self.longitude: str = ''
        self.fix_validity: str = ''
        self.pressure_altitude: str = ''
        self.gps_altitude: str = ''


# H section of IGC file
class Header:
    def __init__(self):
        self.flight_date: datetime.date = datetime.date.today()  # UTC date of flight
        self.fix_accuracy: int = 0
        self.is_pilot_in_charge: bool = False
        self.pilot_name: str = ''
        self.second_pilot_name: str = ''
        self.glider_type: str = ''
        self.glider_id: str = ''
        self.gps_datum: str = ''
        self.gps_datum_num: str = ''

        self.firmware_version: str = ''
        self.hardware_version: str = ''
        self.flight_recorder_type: str = ''
        self.gps_info: GPSInfo = GPSInfo()
        self.pressure_sensor_info: PressureSensorInfo = PressureSensorInfo()
        self.tail_fin_number: str = ''
        self.glider_class: str = ''
        self.time_zone: float = 0.0

    def __str__(self):
        res = str(self.flight_date) + '\n'
        res += 'pilot name: ' + self.pilot_name + '\n'
        res += 'is in charge: ' + str(self.is_pilot_in_charge) + '\n'
        res += 'fix_accuracy: ' + str(self.fix_accuracy) + '\n'
        res += 'second_pilot_name: ' + str(self.second_pilot_name) + '\n'
        res += 'glider_type: ' + str(self.glider_type) + '\n'
        res += 'glider_id: ' + str(self.glider_id) + '\n'
        res += 'gps_datum: ' + str(self.gps_datum) + '\n'
        res += 'gps_datum_number: ' + str(self.gps_datum_num) + '\n'
        res += 'firmware_version: ' + str(self.firmware_version) + '\n'
        res += 'hardware_version: ' + str(self.hardware_version) + '\n'
        res += 'flight_recorder_type: ' + str(self.flight_recorder_type) + '\n'
        res += 'GPS info: ' + str(self.gps_info) + '\n'
        res += 'Pressure sensor info: ' + str(self.pressure_sensor_info) + '\n'
        res += 'Glider class: ' + str(self.glider_class) + '\n'
        res += 'tail fin number: ' + str(self.tail_fin_number) + '\n'
        res += 'timezone: ' + str(self.time_zone) + '\n'

        return res


# L section of IGC file (for 'Logbook' comments)
class Comments:
    def __init__(self):
        self.lines: List[str] = []  # stores raw lines of L section

    def add(self, comment: str):
        self.lines.append(comment)

    def __str__(self):
        return ''.join(self.lines)


# D section of IGC file
class DifferentialGPS:
    def __init__(self):
        self.gps_qualifier: str = ''
        self.dgps_station_id: str = ''

    def __str__(self):
        return 'gps qualifier: ' + self.gps_qualifier + ', ' + 'dgps station id: ' + self.dgps_station_id


# A section of IGC file
class FlightRecorderInfo:
    def __init__(self):
        self.flight_recorder_manufacturer_code: str = 'XXX'
        self.flight_recorder_serial_number: str = ''  # a hex string
        self.daily_flight_number: str = ''

    def __str__(self):
        res = 'FlightRecorderInfo:\n'
        res += 'flight_recorder_manufacturer_code: ' + self.flight_recorder_manufacturer_code + '\n'
        res += 'flight_recorder_serial_number: ' + str(self.flight_recorder_serial_number) + '\n'
        res += 'daily_flight_number: ' + str(self.daily_flight_number) + '\n'

        return res


class FlightInfo:
    def __init__(self):
        self.header = Header()
        self.extension_header = ExtensionHeader()
        self.flight_recorder_info = FlightRecorderInfo()
        self.timed_flight_data: List[TimedFlightData] = []
        self.comments = Comments()
        self.differential_gps: Optional[DifferentialGPS] = None
        self.k_sections: List[KSection] = []
        self.j_section: Optional[JSection] = None

    def __str__(self):
        res = ''
        res += str(self.header) + '\n'
        res += str(self.flight_recorder_info) + '\n'
        res += str(self.extension_header) + '\n'
        res += str(self.comments) + '\n'
        res += str(self.differential_gps) + '\n'
        res += str(self.k_sections) + '\n'
        res += str(self.j_section) + '\n'
        return res
