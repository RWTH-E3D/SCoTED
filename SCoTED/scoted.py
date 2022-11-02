
import numpy as np
import pandas as pd

class SCoTED(object):

    def __init__(self):
        self._weather = None



    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, weather):

        if not isinstance(weather, pd.DataFrame):
            try:
                weather = DataFrame(weather)
            except:
                raise ValueError("Weather has to be in a panda dataframe!")

        self._weather = weather

    def generate_heating_load_curve(self, heat_load_12831, t_standard_12831, t_heating_limit):
        """This function calculates the annual heating load curve from ambient temperature. For this purpose, it
        interpolates linearly between the standard heating load and its standard temperature and the heating limit
        temperature and 0°C.

        Parameters
        ----------
        heat_load_12831: numeric
            Standard heating load according to DIN EN 12831
        t_standard_12831: numeric
            standard temperature according to DIN EN 12831
        t_heating_limit: numeric
            Heating limit temperature
        Returns
        -------
        heating_load_curve : np.array
            Heating load curve in the exact resolution as the weather data stored in the object.

        """

        weather = self.weather.to_numpy()

        heating_load_curve = heat_load_12831 * ((t_heating_limit-weather[:, 1])/(t_heating_limit - t_standard_12831))
        heating_load_curve = heating_load_curve.clip(min = 0)

        return weather[:, 0], heating_load_curve

    def generate_dhw_curve(self):
        pass

    def gernerate_heating_consumption_curve(self):
        pass

    def gernerate_energy_consumption_curve(self):
        pass