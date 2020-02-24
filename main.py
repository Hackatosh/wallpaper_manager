import time

from config import WallpaperChange, Config
from wallpaper import change_wallpaper_based_on_sorted_wcs


def create_test_config() -> None:
    Config.create_default_config_dir()
    wc1 = WallpaperChange('E:\\Edouard\Pictures\wonderbolt_dash_silhouette_wall_by_sambaneko-da81m83.png', 8, 0)
    wc2 = WallpaperChange('E:\\Edouard\Pictures\Wallpaper_Gravity_Falls.png', 20, 00)
    config = Config([wc1, wc2])
    Config.serialize_config(config)

if __name__ == '__main__':
    #TODO POTENTIAL BUG AT MIDNIGHT LOL
    create_test_config()
    config = Config.deserialize_config()
    sorted_wcs = WallpaperChange.sort_by_time_asc(config.wallpaper_changes)
    while True:
        print("TICK")
        change_wallpaper_based_on_sorted_wcs(sorted_wcs)
        time.sleep(60)
