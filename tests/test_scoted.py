from SCoTED.scoted import SCoTED
from SCoTED.weather import Weather
from matplotlib import pyplot as plt
import unittest
from pathlib import Path
import numpy as np


class TestScoted(unittest.TestCase):
    def setUp(self):
        self.dwd_dat_path = Path.cwd() / "testdata" / "TRY2015_37585002676500_Jahr.dat"
        self.sc = SCoTED()

    def test_curve_generator(self):
        temperature = np.array([1, 2, 3, 4, 4])

        point1 = np.array([800, -2])
        point2 = np.array([0, 18])

        result = np.array([680, 640, 600, 560, 560])

        self.assertEqual(self.sc._curve_generator(point1, point2, temperature).tolist(), result.tolist())

    def test_weather(self):
        wp = Weather(self.dwd_dat_path)
        weather = wp.parse("dwd_dat")

        self.sc.weather = weather

        with open(Path.cwd() / "testdata" / "teaser result.npy", "r") as f:
            teaser_data = np.loadtxt(f)
            teaser_heat_load = teaser_data[:8760, 1]

        timestamps, heat_load1 = self.sc.generate_heating_load_curve(heat_load_12831=6200, t_standard_12831=-10.2,
                                                                     t_heating_limit=15)
        timestamps, heat_load2 = self.sc.generate_heating_load_curve(heat_load_12831=6200, t_standard_12831=-10.2,
                                                                     t_heating_limit=11)

        heat_load_sort1 = -np.sort(-heat_load1)
        heat_load_sort2 = -np.sort(-heat_load2)
        teaser_heat_load_sort = -np.sort(-teaser_heat_load)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2)

        # ax1.plot(timestamps,dif)
        ax1.set_ylabel("frequency (-)")
        ax1.set_xlabel("difference (W)")

        ax2.set_ylabel("frequency (-)")
        ax2.set_xlabel("difference (W)")

        ax2.set_xlim([-1000, 1000])
        ax2.set_ylim([0, 800])

        ax1.set_xlim([-1000, 1000])
        ax1.set_ylim([0, 800])

        hours = np.arange(0, 8760, 1, dtype=int)

        dif1 = heat_load_sort1 - teaser_heat_load_sort
        dif2 = heat_load_sort2 - teaser_heat_load_sort

        # ax1.plot(timestamps, heat_load, label = "SCoTED", color="#407FB7")
        # ax1.plot(timestamps, teaser_heat_load, label = "TEASER+", color="#D85C41")

        # ax1.plot(hours, heat_load_sort, label = "SCoTED", color="#00549F")
        # ax1.plot(hours, teaser_heat_load_sort, label = "TEASER+", color="#D85C41")

        # ax2.plot(hours, dif, label="TEASER+ minus SCoTED", color="#8DC060")
        ax1.hist(x=dif2[dif2 != 0], bins=np.arange(-1000, 1000, 20, dtype=int), color="#8DC060")
        ax2.hist(x=dif1[dif1 != 0], bins=np.arange(-1000, 1000, 20, dtype=int), color="#8DC060")

        ax1.legend()
        ax2.legend()
        plt.show()
        """


if __name__ == "__main__":
    unittest.main()
