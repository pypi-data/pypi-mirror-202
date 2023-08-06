from configparser import ConfigParser
from pathlib import Path
import platform
import click
from typing import List
from . import DATA_DIR



default_config_path = Path(__file__).parent / "config.ini"
DEFAULT_CONFIG = ConfigParser()
DEFAULT_CONFIG.read(default_config_path)


# Create config file, copying default config if it doesn't exist
_CONFIG_FILE = DATA_DIR / "config.ini"
if not _CONFIG_FILE.exists():
    if platform.system() == 'Darwin':
        DEFAULT_CONFIG['general']['editor'] = "open"
    elif platform.system() == 'Windows':
        DEFAULT_CONFIG['general']['editor'] = "notepad"
        editor = "notepad.exe"
    else:
        DEFAULT_CONFIG['general']['editor'] = "nano"

    with open(_CONFIG_FILE, "w") as configfile:
        DEFAULT_CONFIG.write(configfile)

CONFIG = ConfigParser()
CONFIG.read(_CONFIG_FILE)


# Add any settings in default_config that don't exist in config file
for section in DEFAULT_CONFIG.sections():
    if section not in CONFIG:
        CONFIG.add_section(section)
    
    for key, value in DEFAULT_CONFIG.items(section):
        if key not in CONFIG[section]:
            CONFIG[section][key] = value

with open(_CONFIG_FILE, "w") as configfile:
    CONFIG.write(configfile)


@click.group("config", help="Configuration")
def config(): 
    """DOCUMENTATION"""
    pass


@config.command()
def show():
    """DOCUMENTATION"""
    print(_CONFIG_FILE.read_text())


@config.command()
def path():
    """DOCUMENTATION"""
    print(str(_CONFIG_FILE.absolute()))


@config.command()
@click.argument("setting", nargs=-1)
@click.argument("value", type=str)
def set(
    setting: List[str],
    value: str
):
    """DOCUMENTATION"""
    config_path = setting
    try:
        dic = CONFIG
        for key in config_path[:-1]:
            dic = dic[key]
        dic[config_path[-1]] = value
    except KeyError as e:
        print(f"{' '.join(setting)} does not exist")

    with open(_CONFIG_FILE, "w") as configfile:
        CONFIG.write(configfile)
