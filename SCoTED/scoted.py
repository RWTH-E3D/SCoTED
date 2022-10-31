
import numpy as np
import pandas as pd

class SCoTED(object):

    def __init__(self):
        self._weather = None
        self.heat_load_12831 = None
        self.t_standard_12831 = None
        self.t_heating_limit = None


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

    def generate_heating_load_curve(self):

        weather = self.weather.to_numpy()

        heating_load_curve = self.heat_load_12831 * ((self.t_heating_limit-weather[:, 1])/(self.t_heating_limit - self.t_standard_12831))
        heating_load_curve = heating_load_curve.clip(min = 0)

        return weather[:, 0], heating_load_curve










    def generate_dhw_curve(self):
        pass

    def gernerate_heating_consumption_curve(self):
        pass

    def gernerate_energy_consumption_curve(self):
        pass