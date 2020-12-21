import unittest
from flight import FlightInfo


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.flight_info = FlightInfo()

    def tearDown(self) -> None:
        self.flight_info = None

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
