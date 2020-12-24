import unittest
from igcparser import IGCParser
from csv_exporter import CSVFlightInfoExporter
import csv


class CSVExporterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = IGCParser('test.igc')
        self.exporter = CSVFlightInfoExporter()
        self.export_file_name = 'test.csv'

    def tearDown(self) -> None:
        self.parser = None
        self.exporter = None

    def test_csv_exporter(self):
        self.exporter.export(self.parser.flight_info, self.export_file_name)

        with open(self.export_file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for (i, row) in enumerate(reader):
                if i == 0:
                    self.assertEqual(row, ['UTC Time', 'Longitude', 'Latitude', 'GPS Alt', 'Fix Validity',
                                           'Pressure Altitude', 'FXA', 'ENL', 'TAS', 'GSP', 'TRT', 'VAT', 'OAT', 'ACZ',
                                           'WDI', 'WVE'])
                elif i == 31:
                    self.assertEqual(row[0], '152310')  # UTC time
                    self.assertEqual(row[1], '07249366W')  # Longitude
                    self.assertEqual(row[2], '4538071N')  # Latitude
                    self.assertEqual(row[3], '00081')  # GPS ALT
                    self.assertEqual(row[4], 'A')  # Fix validity
                    self.assertEqual(row[5], '00022')  # Pressure ALT
                    self.assertEqual(row[6], '007')  # Fix Value
                    self.assertEqual(row[7], '001')  # ENL
                    self.assertEqual(row[8], '10454')  # TAS
                    self.assertEqual(row[9], '12720')  # GSP
                    self.assertEqual(row[10], '314')  # TRT
                    self.assertEqual(row[11], '00192')  # VAT
                    self.assertEqual(row[12], '0242')  # OAT
                    self.assertEqual(row[13], '0130')  # ACZ


if __name__ == '__main__':
    unittest.main()
