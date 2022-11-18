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
                weather = pd.DataFrame(weather)
            except TypeError:
                raise TypeError("Weather has to be in a panda dataframe or a compatible format!")

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
            Standard temperature according to DIN EN 12831
        t_heating_limit : numeric
            Heating limit temperature
        Returns
        -------
        heating_load_curve : numpy.array
            Heating load curve in the exact resolution as the weather data stored in the object.

        """

        reference_point1 = np.array([heat_load_12831, t_standard_12831])
        reference_point2 = np.array([0, t_heating_limit])

        heating_load_curve = self._curve_generator(reference_point1, reference_point2)
        heating_load_curve.clip(min=0, out=heating_load_curve)

        return self.weather[:, 0], heating_load_curve

    def _curve_generator(self, point1, point2):
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
            Generated curve

        """

        if not numpy.array_equal(point1, point2):
            curve = point1[0] + ((point2[0] - point1[0]) / (point2[1] - point1[1])) * (temperature_curve - point1[1])
        else:
            raise ValueError("Linear interpolation requires 2 different points, but two identical were given!")

        return curve

    def generate_dhw_curve(self, test):

        pass

    def gernerate_heating_consumption_curve(self, heating_consumption, t_standard_12831, t_heating_limit):
        """This function calculates the annual heating energy consumption curve from the ambient temperature.


        Parameters
        ----------
        heating_consumption : numeric
            Annual energy consumption for heating the building
        t_standard_12831 : numeric
            Standard heating load according to DIN EN 12831
        t_heating_limit : numeric
            Standard temperature according to DIN EN 12831
        Returns
        -------
        heating_load_curve : numpy.array
            Heating load curve in the exact resolution as the weather data stored in the object.
        """

        g = (t_heating_limit - self.weather[:, 1])
        g = g.clip(min=0)
        b_vf = g / (t_heating_limit - t_standard_12831)
        heating_load = heating_consumption / b_vf

        return generate_heating_load_curve(heating_load, t_standard_12831, t_heating_limit)

    def gernerate_energy_consumption_curve(self):
        pass
