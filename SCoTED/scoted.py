import numpy
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

        self._weather = weather.to_numpy()

    def generate_heating_load_curve(self, heat_load_12831, t_standard_12831, t_heating_limit):
        """This function calculates the annual heating load curve from ambient temperature. For this purpose, it
        interpolates linearly between the standard heating load and its standard temperature and the heating limit
        temperature and 0°C.

        Parameters
        ----------
        heat_load_12831 : numeric
            Standard heating load according to DIN EN 12831
        t_standard_12831 : numeric
            standard temperature according to DIN EN 12831
        t_heating_limit : numeric
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

    def _curve_generator(self, point1, point2, temperature_curve):
        """These functions interpolate for each value of a temperature curve the heating load from two data points
        (point1, point2)

        Parameters
        ----------
        point1 : numpy.array
            First data point for linear interpolation consisting of a heat load and a coresponding temperature.
            The format is [heat_load, temperature].
        point2 : numpy.array
            Second data point for linear interpolation consisting of a heat load and a coresponding temperature.
            The format is [heat_load, temperature].

        Returns
        -------
        curve : numpy.array
            generated curve

        """

        if not numpy.array_equal(point1, point2):
            curve = point1[0] + ((point2[0]-point1[0])/(point2[1]-point1[1])) * (temperature_curve-point1[1])
        else:
            raise ValueError("Linear interpolation requires 2 different points, but two identical were given!")

        return curve


    def generate_dhw_curve(self, test):

        pass

    def gernerate_heating_consumption_curve(self):
        pass

    def gernerate_energy_consumption_curve(self):
        pass