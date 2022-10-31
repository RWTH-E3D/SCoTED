from SCoTED.weather import Weather
import unittest
from pathlib import Path

class TestWeatherParser(unittest.TestCase):
    def setUp(self):
        self.dwd_dat_path = Path.cwd() / "testdata" / "TRY2015_37585002676500_Jahr.dat"


    def test_parse(self):

        wp = Weather(self.dwd_dat_path)
        wp.parse("dwd_dat")


if __name__ == "__main__":
     unittest.main()