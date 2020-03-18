# Wallpaper Changer Project

Welcome to the repository of Wallpaper Changer !

This project is a personal project started in February 2020. 
The goal of the project is to provide a little service to change your wallpaper automatically at predefined hours,
allowing you to have different wallpaper for the morning and the evening as an example, a functionality which does
not exist natively in Windows.

## Getting Started

These instructions will help you get Wallpaper Changer running !

### Prerequisites

Before being able to run this project, you need to fulfill the following requirements :

* A PC with Windows 10 64 Bits (it his the only OS on which the project was tested).
* [Python 3](https://www.python.org/), with the 3.7.4 version (the application is not packaged for the moment).

### Launch the application

To launch the application, simply use : 

```
python main.py
```

To launch the application in the background, use :

```
pythonw main.py
```

On Windows, I recommend to use the Task Scheduler to start the script in the background at the start of the system.

### Edit the configuration file

For now, only a default location for the configuration file is supported. 
The default location is _C:\Users\username\.wallpaper_changer\config.ini_.

The configuration file looks like this :

```
[wallpaper_change.0]
absolute_path = E:\Edouard\Pictures\Wallpapers\pine_twins.png
hour = 7
minute = 30

[wallpaper_change.1]
absolute_path = E:\Edouard\Pictures\Wallpapers\7595.jpg
hour = 13
minute = 30

[wallpaper_change.2]
absolute_path = E:\Edouard\Pictures\Wallpapers\Wallpaper_Gravity_Falls.png
hour = 20
minute = 30
```

To add a wallpaper change, just add an other key. You can also easily edit the absolute path to the wallpaper 
(_absolute_path_) and the time of the change (_hour_ and _minute_).

As the config file is loaded only once at the start of the application, 
the changes are effective only after the application is restarted. 

## What's coming next ?

If I have the time, the following features will be added in the future :
- A GUI to define your wallpaper changes
- Support for other OS (only Windows 10 64 bits is officially supported for now)
- Package the application to allows users to run it without installing Python
- Extend the application with other trigger for wallpaper changes

## Built With

The whole project is written in [Python 3](https://www.python.org/). 

## Author

* Edouard Benauw - [Hackatosh](https://github.com/Hackatosh)

## Contributing

If you want to contribute, please contact me !

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* The StackOverflow user *abdusco* for posting a useful snippet which I use to make the wallpaper transition.
* The [Chameleon project](https://github.com/ianmartinez/Chameleon) which is an inspiration for this project.