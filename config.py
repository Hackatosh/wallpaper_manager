import configparser
import datetime
import os
from typing import List

from time_helpers import get_time_at


class WallpaperChange:
    """
    This object represents a wallpaper change which will be executed every day.
    It holds the absolute path to the wallpaper and the time at which the change has to be executed (hour and minute).
    """

    def __init__(self, absolute_path: str, hour: int, minute: int):
        self.__absolute_path = absolute_path
        self.__hour = hour
        self.__minute = minute

    @property
    def absolute_path(self) -> str:
        return self.__absolute_path

    @property
    def hour(self) -> int:
        return self.__hour

    @property
    def minute(self) -> int:
        return self.__minute

    @property
    def time_at(self) -> datetime:
        return get_time_at(self.__hour, self.__minute)

    def __str__(self):
        return f'WallpaperChange : {{absolute_path : {self.absolute_path}, hour : {self.hour}, minute : {self.minute}}}'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def sort_by_time_asc(cls, wc_list: List["WallpaperChange"]) -> List["WallpaperChange"]:
        """
        Sort the list of wallpaper changes provided by ascending time, using the method provided in time_helpers.
        The method returns a new list and does not sort in place.
        """
        return sorted(wc_list, key=lambda wc: wc.time_at)


class Config:
    """
    This object represents the configuration of the whole application.
    It has static methods used for serialization / deserialization using the configparser package of Python and various
    helpers.
    For now, it only holds the list of wallpaper changes.
    """

    def __init__(self, wallpaper_changes: List[WallpaperChange]):
        self.__wallpaper_changes = wallpaper_changes

    @property
    def wallpaper_changes(self) -> List[WallpaperChange]:
        return self.__wallpaper_changes

    def __str__(self):
        return f"Config : {{wallpaper_changes : {self.wallpaper_changes}}}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_default_config_path(cls) -> str:
        """
        Returns the default path of the configuration file.
        The default path is ~/.wallpaper_changer/config.ini.
        """
        return os.path.join(os.path.expanduser("~"), '.wallpaper_changer', 'config.ini')

    @classmethod
    def get_default_config_dir(cls) -> str:
        """
        Returns the default path of the configuration folder.
        The default path is ~/.wallpaper_changer/.
        """
        return os.path.join(os.path.expanduser("~"), '.wallpaper_changer')

    @classmethod
    def create_default_config_dir(cls) -> None:
        """
        Create the configuration folder at the default path specified by get_default_config_dir.
        """
        path = Config.get_default_config_dir()
        if os.path.isdir(path):
            print(f"Config directory already exists !")
            return
        try:
            os.mkdir(path)
        except OSError:
            print(f"Creation of the config directory at {path} failed")
        else:
            print(f"Successfully created the config directory at {path}")

    @classmethod
    def get_wc_key(cls, index: int) -> str:
        """
        A simple helper for serialization/deserialization which automatically format the key used to access ONE wallpaper
        change in the LIST of wallpaper changes.
        """
        return f'wallpaper_change.{index}'

    @classmethod
    def serialize_config(cls, config: "Config", absolute_path: str = None) -> None:
        """
        Method used to serialize the Config object provided in a configuration file which will be stored at the absolute path
        provided.
        If no path is provided, it uses the default configuration path.
        The method use the configparser Python package.
        """
        if absolute_path is None:
            absolute_path = cls.get_default_config_path()
        config_p = configparser.ConfigParser()
        for index, wc in enumerate(config.wallpaper_changes):
            key = Config.get_wc_key(index)
            config_p[key] = {}
            config_p[key]["absolute_path"] = wc.absolute_path
            config_p[key]["hour"] = str(wc.hour)
            config_p[key]["minute"] = str(wc.minute)
        with open(absolute_path, 'w') as configfile:
            config_p.write(configfile)

    @classmethod
    def deserialize_config(cls, absolute_path: str = None) -> "Config":
        """
        Method used to deserialize the configuration file located at the absolute_path provided into a Config object.
        If no path is provided, it uses the default configuration path.
        The method use the configparser Python package.
        """
        if absolute_path is None:
            absolute_path = cls.get_default_config_path()
        config_p = configparser.ConfigParser()
        config_p.read(absolute_path)
        index = 0
        key = Config.get_wc_key(index)
        wc_list = []
        while key in config_p:
            absolute_path = config_p[key]["absolute_path"]
            hour = int(config_p[key]["hour"])
            minute = int(config_p[key]["minute"])
            wc_list.append(WallpaperChange(absolute_path, hour, minute))
            index += 1
            key = Config.get_wc_key(index)
        return Config(wc_list)
