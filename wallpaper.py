import os
import struct
import ctypes
from typing import List
from datetime import datetime
import pythoncom
import pywintypes
import win32gui
from win32com.shell import shell, shellcon
from config import WallpaperChange

LATEST_WP_CHANGE = ""  # Global variable that will be modified to hold the latest change to prevent useless changes

"""CUSTOM WALLPAPER CHANGE WITHOUT ANY TRANSITION"""

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


"""WALLPAPER CHANGE WITH TRANSITION"""
"""Snippet found on : https://stackoverflow.com/questions/56973912/how-can-i-set-windows-10-desktop-background-with-smooth-transition/56974396#56974396"""

user32 = ctypes.windll.user32


def _make_filter(class_name: str, title: str):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows"""

    def enum_windows(handle: int, h_list: list):
        if not (class_name or title):
            h_list.append(handle)
        if class_name and class_name not in win32gui.GetClassName(handle):
            return True  # continue enumeration
        if title and title not in win32gui.GetWindowText(handle):
            return True  # continue enumeration
        h_list.append(handle)

    return enum_windows


def find_window_handles(parent: int = None, window_class: str = None, title: str = None) -> List[int]:
    cb = _make_filter(window_class, title)
    try:
        handle_list = []
        if parent:
            win32gui.EnumChildWindows(parent, cb, handle_list)
        else:
            win32gui.EnumWindows(cb, handle_list)
        return handle_list
    except pywintypes.error:
        return []


def force_refresh():
    user32.UpdatePerUserSystemParameters(1)


def enable_activedesktop():
    """https://stackoverflow.com/a/16351170"""
    try:
        progman = find_window_handles(window_class='Progman')[0]
        cryptic_params = (0x52c, 0, 0, 0, 500, None)
        user32.SendMessageTimeoutW(progman, *cryptic_params)
    except IndexError as e:
        raise WindowsError('Cannot enable Active Desktop') from e


def change_wallpaper_unsafe_active_desktop(image_path: str, use_activedesktop: bool = True):
    if use_activedesktop:
        enable_activedesktop()
    pythoncom.CoInitialize()
    iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop,
                                     None,
                                     pythoncom.CLSCTX_INPROC_SERVER,
                                     shell.IID_IActiveDesktop)
    iad.SetWallpaper(str(image_path), 0)
    iad.ApplyChanges(shellcon.AD_APPLY_ALL)
    force_refresh()


""" COMMON STUFF FOR CHANGING WALLPAPER"""


def check_if_file_exist(absolute_path: str) -> bool:
    if os.path.isfile(absolute_path):
        return True
    else:
        return False


def change_wallpaper_safe(absolute_path: str, use_transition: bool = True) -> None:
    if check_if_file_exist(absolute_path):
        if use_transition:
            change_wallpaper_unsafe_active_desktop(absolute_path)
        else:
            change_wallpaper_unsafe(absolute_path)
        print(f'Wallpaper changed successfully by the file located at {absolute_path}.')
    else:
        print(f'The file located at {absolute_path} does not exist. The wallpaper has not been changed.')


def change_wallpaper_based_on_sorted_wcs(wcs: List[WallpaperChange]) -> None:
    global LATEST_WP_CHANGE  # TODO Use API to check the current wallpaper instead of this
    change_to_do = wcs[-1]
    now = datetime.now()
    for wc in wcs:
        if wc.time_at < now:
            change_to_do = wc
    path = change_to_do.absolute_path
    if change_to_do is not None and path != LATEST_WP_CHANGE:
        LATEST_WP_CHANGE = path
        change_wallpaper_safe(path)

if __name__ == '__main__':
    change_wallpaper_safe(r'E:\Edouard\Pictures\Wallpapers\Wallpaper_Gravity_Falls.png')