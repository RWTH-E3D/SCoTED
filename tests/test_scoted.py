from SCoTED.scoted import SCoTED
from SCoTED.weather import Weather
from matplotlib import pyplot as plt
import unittest
from pathlib import Path
import numpy as np


class TestWeatherParser(unittest.TestCase):
    def setUp(self):
        self.dwd_dat_path = Path.cwd() / "testdata" / "TRY2015_37585002676500_Jahr.dat"
        self.sc = SCoTED()


    def test_weather(self):

        wp = Weather(self.dwd_dat_path)
        weather = wp.parse("dwd_dat")

        self.sc.weather = weather

        timestamps, heat_load = self.sc.generate_heating_load_curve(heat_load_12831 = 1200, t_standard_12831 = -10.5, t_heating_limit = 15)

        timestamps2, heat_load2 = self.sc.generate_heating_load_curve(heat_load_12831=1200, t_standard_12831=-10.5, t_heating_limit=18)

        heat_load_sort = -np.sort(-heat_load)
        heat_load2_sort = -np.sort(-heat_load2)

        print(heat_load_sort)

        fig, (ax1, ax2) = plt.subplots(1,2)

        #dif = heat_load_sort - heat_load2_sort

        #ax1.plot(timestamps,dif)

        ax1.plot(timestamps, heat_load, '.', markersize = 0.5)
        ax1.plot(timestamps2, heat_load2, '.', markersize = 0.5 )

        ax2.plot(timestamps, heat_load_sort)
        ax2.plot(timestamps2, heat_load2_sort)

        plt.show()



if __name__ == "__main__":
     unittest.main()