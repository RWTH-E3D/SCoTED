import pandas as pd
from pathlib import Path
import re
import datetime

class Weather(object):

    def __init__(self, weather_file_path):
        self.path = weather_file_path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, weather_file_path):

        if not isinstance(weather_file_path, Path):
            try:
                weather_file_path = Path(weather_file_path)
            except:
                raise ValueError("The path to the weather dataset contains an error!")

        self._path = weather_file_path

    def parse(self, format, path=None):
        if path != None:
            self.path = path

        format_dict = {"dwd_dat": self._parse_dwd_dat}

        if format in format_dict:
            return format_dict[format]()
        else:
            raise ValueError(f"Unknown weather data format {format}!")




    def _parse_dwd_dat(self):

        if self.path.suffix == ".dat":
            with open(self.path, "r") as f:
                f_list = f.readlines()

                data_start = f_list.index('*** \n') + 1
                f_list = f_list [data_start:]


                f_str = "".join(f_list)


                f_str = re.sub(' +', ' ', f_str)

                if f_str.startswith(" "):
                    f_str = f_str[1:]
                columns = ["RW", "HW", "MM", "DD", "HH", "temperature", "p", "WR", "Wg", "N","x", "RF", "B", "D" , "A", "E", "IL"]
                df = pd.DataFrame([row.split(' ') for row in f_str.split('\n')], columns=columns)

                today = datetime.date.today()
                year = today.year

                timestamps = []

                df.drop(index=df.index[-1], axis=0, inplace=True)

                for index, row in df.iterrows():

                    dt = datetime.datetime(year, int(row["MM"]), int(row ["DD"]), int(row["HH"])-1)
                    timestamps.append(dt)

                df.insert(0, "timestamp", timestamps, True)
                df = df[["timestamp", "temperature"]]
                df["temperature"] = pd.to_numeric(df["temperature"])

                return df



        else:
            raise ValueError("DWD dat file should end with *.dat!")

        print("huhu")


