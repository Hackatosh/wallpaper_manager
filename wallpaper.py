import os
import struct
import ctypes
from typing import List
from datetime import datetime

from config import WallpaperChange

SPI_SETDESKWALLPAPER = 20
LATEST_WP_CHANGE = ""  # Global variable that will be modified to hold the latest change to prevent useless changes


def is_64_windows() -> bool:
    """Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def change_wallpaper_unsafe(absolute_path: str) -> None:
    sys_parameters_info = get_sys_parameters_info()
    r = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, absolute_path, 3)
    # When the SPI_SETDESKWALLPAPER flag is used,
    # SystemParametersInfo returns TRUE
    # unless there is an error (like when the specified file doesn't exist).
    if not r:
        print(ctypes.WinError())


def check_if_file_exist(absolute_path: str) -> bool:
    if os.path.isfile(absolute_path):
        return True
    else:
        return False


def change_wallpaper_safe(absolute_path: str) -> None:
    if check_if_file_exist(absolute_path):
        change_wallpaper_unsafe(absolute_path)
        print(f'Wallpaper changed successfully by the file located at {absolute_path}.')
    else:
        print(f'The file located at {absolute_path} does not exist. The wallpaper has not been changed.')


def change_wallpaper_based_on_sorted_wcs(wcs: List[WallpaperChange]) -> None:
    global LATEST_WP_CHANGE #TODO Use API to check the current wallpaper instead of this
    change_to_do = wcs[0]
    now = datetime.now()
    for wc in wcs:
        if wc.time_at < now:
            change_to_do = wc
    path = change_to_do.absolute_path
    if change_to_do is not None and path != LATEST_WP_CHANGE:
        LATEST_WP_CHANGE = path
        change_wallpaper_safe(path)
