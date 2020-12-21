import unittest
from flight import FlightInfo
from parser import IGCParser


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.flight_info = FlightInfo()

    def tearDown(self) -> None:
        self.flight_info = None

    def test_parse_flight_recorder_info(self):
        parser = IGCParser()
        parser.flight_info = self.flight_info
        parser._parse_flight_recorder_info('AFLA9WL')
        self.assertEqual(self.flight_info.flight_recorder_info.flight_recorder_manufacturer_code, 'FLA')


if __name__ == '__main__':
    unittest.main()
