import os
import struct
import ctypes

SPI_SETDESKWALLPAPER = 20


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
    else:
        print(f'The file located at {absolute_path} does not exist. The wallpaper has not been changed.')

if __name__ == '__main__':
    path = 'E:\\Edouard\Pictures\wonderbolt_dash_silhouette_wall_by_sambaneko-da81m83.png'
    change_wallpaper_safe(path)
    path = 'E:\\Edouard\Pictures\wla.txt'
    change_wallpaper_safe(path)
