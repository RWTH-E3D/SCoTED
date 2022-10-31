from SCoTED.scoted import SCoTED
from SCoTED.weather import Weather
from matplotlib import pyplot as plt
import unittest
from pathlib import Path

class TestWeatherParser(unittest.TestCase):
    def setUp(self):
        self.dwd_dat_path = Path.cwd() / "testdata" / "TRY2015_37585002676500_Jahr.dat"
        self.sc = SCoTED()


    def test_weather(self):

        wp = Weather(self.dwd_dat_path)
        weather = wp.parse("dwd_dat")

        self.sc.weather = weather
        self.sc.heat_load_12831 = 1200
        self.sc.t_standard_12831 = -10.5
        self.sc.t_heating_limit = 15
        timestamps, heat_load = self.sc.generate_heating_load_curve()

        plt.plot(timestamps, heat_load)
        plt.show()



if __name__ == "__main__":
     unittest.main()