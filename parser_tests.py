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

    def test_extension_header(self):
        self.parser._parse_extension_header('I023638FXA3940SIU')
        self.assertEqual(self.flight_info.extension_header.num_extensions, 2)
        self.assertEqual(self.flight_info.extension_header.flight_data['FXA'], (36, 38))
        self.assertEqual(self.flight_info.extension_header.flight_data['SIU'], (39, 40))

    def test_basic_timed_flight_data(self):
        # No additional info was found
        self.parser._parse_timed_flight_data('B1511094538002N07249279WA-00940004000109')
        timed_data_list = self.flight_info.timed_flight_data
        self.assertEqual(len(timed_data_list), 1)
        timed_data = timed_data_list[0]
        self.assertIsNone(timed_data.extensions)
        self.assertEqual(timed_data.utc_time, '151109')
        self.assertEqual(timed_data.latitude, '4538002N')
        self.assertEqual(timed_data.longitude, '07249279W')
        self.assertEqual(timed_data.fix_validity, 'A')
        self.assertEqual(timed_data.pressure_altitude, '-0094')
        self.assertEqual(timed_data.gps_altitude, '00040')

    def test_full_extended_timed_flight_data(self):
        self.parser._parse_extension_header('I023638FXA3940SIU')
        self.parser._parse_timed_flight_data('B1511094538002N07249279WA-00940004000109')

        indices_to_title = {(36, 38): 'FXA', (39, 40): 'SIU'}
        title_to_value = {}  # string to string

        timed_data_list = self.flight_info.timed_flight_data
        self.assertEqual(len(timed_data_list), 1)
        timed_data = timed_data_list[0]
        self.assertIsNotNone(timed_data.extensions)

        for info_data in timed_data_list:
            for indices in info_data.extensions.values():
                title = indices_to_title[(indices[0], indices[1])]
                title_to_value[title] = info_data.raw_data[indices[0]:indices[1]+1]

        self.assertEqual(title_to_value['FXA'], '010')
        self.assertEqual(title_to_value['SIU'], '9')


if __name__ == '__main__':
    unittest.main()
