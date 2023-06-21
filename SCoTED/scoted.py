import numpy
import numpy as np
import pandas as pd
import json
import os


class SCoTED(object):

    def __init__(self):
        self._weather = None
        self._dhw_profiles = self.load_dhw_profiles()

    @staticmethod
    def load_dhw_profiles():
        dhw_profiles_path = os.path.join(os.path.abspath(os.curdir), "..", "tests", "testdata",
                                         "dhw_profiles.json")
        with open(dhw_profiles_path) as f:
            dhw_profiles = json.load(f)
        return dhw_profiles

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

    def _curve_generator(self, point1, point2, temperature=None):
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
        if temperature is None:
            if self.weather is None:
                raise ValueError("Please specify a weather dataset in the object or assign it to the function ")
            else:
                temperature = self.weather[:, 1]
        if not numpy.array_equal(point1, point2):
            curve = point1[0] + ((point2[0] - point1[0]) / (point2[1] - point1[1])) * (temperature - point1[1])
        else:
            raise ValueError("Linear interpolation requires 2 different points, but two identical were given!")

        return curve

    def generate_dhw_curve(self, heating_consumption_dhw=None, heating_consumption=None, percentage_dhw=None,
                           dhw_profile_name=None):
        """This function calculates the hourly domestic hot water (dhw) profile based on a given annual energy/ heating
        consumption for dhw (or based on a given annual heating consumption and the percentage of dhw) and
        a 24h tap profile (dhw profile) located in a json file.

        Parameters
        ----------
        heating_consumption_dhw: numeric
            Annual energy consumption for dhw [Wh].
        heating_consumption: numeric
            Annual energy consumption for heating the building [Wh]
        percentage_dhw: numeric
            Percentage of dhw in annual energy consumption in decimal [-]
        dhw_profile_name: string
            Name of the dhw profile to be used. Default profile is "average_single_person", which is taken from the
            DIN 15450. The other profiles available are "average_family" and "average_threeheaded_family"

        Returns
        -------
        numpy.array
            Generated array with hourly (8760) values for dhw energy consumption [W]
        """

        if heating_consumption and percentage_dhw is not None:
            load_value = heating_consumption * percentage_dhw
        elif heating_consumption_dhw is not None:
            load_value = heating_consumption_dhw
        else:
            raise Exception("Either a value for the dhw heating consumption must be given, or in case"
                            "of a given total energy consumption, the percentage of dhw is needed.")

        if dhw_profile_name is not None:
            try:
                used_profile = np.array(self._dhw_profiles["dhw_profiles"][dhw_profile_name])
            except Exception:
                raise Exception("No viable dhw profile name was passed. Available profiles:\n"
                                "'average_single_person', 'average_family', 'average_threeheaded_family'\n"
                                "If no profile name is given, default profile 'average_single_person' is used")
        else:
            used_profile = np.array(self._dhw_profiles["dhw_profiles"]["average_single_person"])

        sum_over_year = sum(used_profile) * 365
        dhw_norm_day = used_profile / sum_over_year
        dhw_profile = load_value * dhw_norm_day

        return np.tile(dhw_profile, 365)

    def generate_cooling_load_curve(self, cooling_load_2078, t_standard, t_cooling_limit, adjustment=False):
        """This function calculates the annual cooling load curve from ambient temperature. For this purpose, it
        interpolates linearly between the standard cooling load and its standard temperature and the cooling limit
        temperature and 0W.
        The option to reduce the loads which exceed the stated cooling_load_2078 (in case the maximum
        temperature from the weather data set is greater than t_standard) divides each load value by
        the calculated adjustment factor.

        Parameters
        ----------
        cooling_load_2078 : numeric
            Standard cooling load according to VDI 2078 [W]
        t_standard : numeric
            Standard temperature belonging to the cooling load [°C]
        t_cooling_limit : numeric
            cooling limit temperature [°C]
        adjustment : boolean
            if true, the adjustment factor to reduce the maximum loads to the given cooling_load_2078
            is used in case the maximum temperature from the weather data set is greater than t_standard
        Returns
        -------
        cooling_load_curve : numpy array
            Cooling load curve in the exact resolution as the weather data stored in the object. [W]

        """

        reference_point1 = np.array([cooling_load_2078, t_standard])
        reference_point2 = np.array([0, t_cooling_limit])

        cooling_load_curve = self._curve_generator(reference_point1, reference_point2, temperature=None)
        cooling_load_curve.clip(min=0, out=cooling_load_curve)

        max_temp = self.weather[:, 1].max()
        if adjustment is True and max_temp > t_standard:
            print("Adjustment is made"
                  "\nCaution: Cooling load is reduced")
            adjustment_factor = (max_temp - t_cooling_limit) / (t_standard - t_cooling_limit)
            cooling_load_curve = cooling_load_curve / adjustment_factor
        elif adjustment is True and max_temp < t_standard:
            print("No adjustment required: Maximum temperature from weather data set < t_standard")
        elif adjustment is False and max_temp > t_standard:
            print("Adjustment is set to False"
                  "\nMaximum temperature from weather data set is greater than the standard temperature belonging "
                  "to the given cooling load"
                  "\nCooling loads greater than those given in the function call may occur")
        else:
            print("No adjustment is made")

        return self.weather[:, 0], cooling_load_curve

    def generate_cooling_consumption_curve(self, cooling_consumption, t_cooling_limit):
        """This function calculates the annual cooling energy consumption curve from the ambient temperature.

        Parameters
        ----------
        cooling_consumption : numeric
            Annual energy consumption for heating the building [Wh]
        t_cooling_limit : numeric
            Cooling limit temperature [°C]
        Returns
        -------
        cooling_load_curve : numpy array
            Cooling load curve in the exact resolution as the weather data stored in the object. [W]
        """
        if self.weather is None:
            raise ValueError("Please specify a weather dataset in the object")
        else:
            temperature = self.weather[:, 1]

        cooling_hours = (temperature - t_cooling_limit) * 10  # for 0.1 degree C steps
        sum_cooling_hours = np.sum(cooling_hours[cooling_hours > 0])
        b = cooling_consumption / sum_cooling_hours  # [W/0.1°C]

        cooling_load_curve = np.zeros(8760)
        for i in range(8760):
            if cooling_hours[i] >= 0:
                cooling_load_curve[i] = b * 10 * (temperature[i] - t_cooling_limit)
        # cooling_load_curve = b * 10 * (temperature - t_cooling_limit)
        cooling_load_curve.clip(min=0, out=cooling_load_curve)

        return self.weather[:, 1], cooling_load_curve

    def generate_heating_consumption_curve(self, heating_consumption, t_standard_12831, t_heating_limit):
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
        G = np.sum(g[g > 0])
        b_vf = G / (t_heating_limit - t_standard_12831)
        heating_load = heating_consumption / b_vf

        reference_point1 = np.array([heating_load, t_standard_12831])
        reference_point2 = np.array([0, t_heating_limit])

        heating_load_curve = self._curve_generator(reference_point1, reference_point2, self.weather[:, 1])
        heating_load_curve.clip(min=0,  out=heating_load_curve)

        return self.weather[:, 0], heating_load_curve

    def gernerate_energy_consumption_curve(self):
        pass
