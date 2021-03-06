import unittest
from flight import FlightInfo
from igcparser import IGCParser, ParseError


class ParserTests(unittest.TestCase):

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

    def test_j_and_k_sections_1(self):
        self.parser._parse_j_section('J010810HDT')
        self.parser._parse_k_section('K160310090')

        self.assertEqual(self.flight_info.j_section.num_extensions, 1)
        self.assertEqual(self.flight_info.k_sections[0].flight_data_values['HDT'], '090')
        self.assertEqual(self.flight_info.k_sections[0].utc_timestamp, '160310')

    def test_j_and_k_sections_2(self):
        self.parser._parse_j_section('J020810WDI1115WVE')
        self.parser._parse_k_section('K08570707200057')

        self.assertEqual(self.flight_info.j_section.num_extensions, 2)
        self.assertEqual(self.flight_info.k_sections[0].flight_data_values['WVE'], '00057')
        self.assertEqual(self.flight_info.k_sections[0].flight_data_values['WDI'], '072')
        self.assertEqual(self.flight_info.k_sections[0].utc_timestamp, '085707')

    def test_parse_k_section_without_j_section(self):
        self.assertRaises(ParseError, self.parser._parse_k_section, 'KTHISISATESTKSECTION')


if __name__ == '__main__':
    unittest.main()
