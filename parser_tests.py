import unittest
from flight import FlightInfo
from parser import IGCParser


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.flight_info = FlightInfo()
        self.parser = IGCParser()
        self.parser.flight_info = self.flight_info

    def tearDown(self) -> None:
        self.flight_info = None
        self.parser = None

    def test_parse_flight_recorder_info(self):
        self.parser._parse_flight_recorder_info('AFLA9WL')
        self.assertEqual(self.flight_info.flight_recorder_info.flight_recorder_manufacturer_code, 'FLA')
        self.assertEqual(self.flight_info.flight_recorder_info.flight_recorder_serial_number, '9WL')

    def test_extension_header(self):
        self.parser._parse_extension_header('I023638FXA3940SIU')
        self.assertEqual(self.flight_info.extension_header.num_extensions, 2)
        self.assertEqual(self.flight_info.extension_header.extended_data_indices['FXA'], (36, 38))
        self.assertEqual(self.flight_info.extension_header.extended_data_indices['SIU'], (39, 40))

    def test_basic_timed_flight_data(self):
        # No additional info was found
        self.parser._parse_timed_flight_data('B1511094538002N07249279WA-00940004000109')
        timed_data_list = self.flight_info.timed_flight_data
        self.assertEqual(len(timed_data_list), 1)
        timed_data = timed_data_list[0]
        self.assertIsNone(timed_data.extension_values)
        self.assertEqual(timed_data.utc_time, '151109')
        self.assertEqual(timed_data.latitude, '4538002N')
        self.assertEqual(timed_data.longitude, '07249279W')
        self.assertEqual(timed_data.fix_validity, 'A')
        self.assertEqual(timed_data.pressure_altitude, '-0094')
        self.assertEqual(timed_data.gps_altitude, '00040')

    def test_full_extended_timed_flight_data(self):
        self.parser._parse_extension_header('I023638FXA3940SIU')
        self.parser._parse_timed_flight_data('B1511094538002N07249279WA-00940004000109')

        self.assertEqual(len(self.flight_info.timed_flight_data), 1)

        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['FXA'], '001')
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['SIU'], '09')

    def test_complex_extended_timed_flight_data(self):
        self.parser._parse_extension_header('I083638FXA3941ENL4246TAS4751GSP5254TRT5559VAT6063OAT6467ACZ')
        self.parser._parse_timed_flight_data('B1723034538174N07249500WA000080011200701212277143713160034802090098')

        self.assertEqual(len(self.flight_info.timed_flight_data), 1)

        self.assertEqual(self.flight_info.extension_header.num_extensions, 8)
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['FXA'], '007')
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['ENL'], '012')
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['TAS'], '12277')
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['GSP'], '14371')
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['TRT'], '316')
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['VAT'], '00348')
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['OAT'], '0209')
        self.assertEqual(self.flight_info.timed_flight_data[0].extension_values['ACZ'], '0098')





if __name__ == '__main__':
    unittest.main()
