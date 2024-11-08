"""
This code defines a class which holds the config values for His Majesty's
Software Suite.
"""

# Standard imports.
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self

# Local constants.
DEFAULT_GIT_ACCOUNT_NAME = "tomhosker"
DEFAULT_CLONE_METHOD = "https"
DEFAULT_GIT_HOST = "github.com"
JSON_INDENT = 4
# Lists.
DEFAULT_ESSENTIAL_APT_PACKAGES = ("git", "gedit-plugins")
DEFAULT_NON_ESSENTIAL_APT_PACKAGES = ("inkscape", "vlc")
DEFAULT_ROYAL_REPOS = (
    "celanta_at_the_well_of_life",
    "chancery",
    "chancery_b",
    "hgmj",
    "hoskers_almanack",
    "hosker_utils",
    "lucifer_in_starlight",
    "reading_room",
    "vanilla_web"
)
# Paths.
PATH_OBJ_TO_HERE = Path(__file__).parent
PATH_TO_DEFAULT_WALLPAPER_DIR = str(PATH_OBJ_TO_HERE/"wallpaper")
PATH_TO_HMSS_CONFIG = str(Path.home()/"hmss_config.json")
# Dicts.
DEFAULT_HMSS_CONFIG = {
    "thunderbird_num": None,
    "essential_apt_packages": DEFAULT_ESSENTIAL_APT_PACKAGES,
    "non_essential_apt_packages": DEFAULT_NON_ESSENTIAL_APT_PACKAGES,
    "path_to_wallpaper_file": None,
    "install_chrome": False,
    "royal_repos": DEFAULT_ROYAL_REPOS,
    "clone_method": DEFAULT_CLONE_METHOD,
    "git_host": DEFAULT_GIT_HOST,
    "git_account_name": DEFAULT_GIT_ACCOUNT_NAME
}

##############
# MAIN CLASS #
##############

@dataclass
class HMSSConfig:
    """ The class in question. """
    thunderbird_num: int|None = None
    essential_apt_packages: list[str]|None = None
    non_essential_apt_packages: list[str]|None = None
    path_to_wallpaper_file: str|None = None
    install_chrome: bool|None = False
    royal_repos: list[str]|None = None
    clone_method: str|None = None
    git_host: str|None = None
    git_account_name: str|None = None

    def __post_init__(self):
        if not self.path_to_wallpaper_file:
            self._set_path_to_wallpaper_file()

    def _set_path_to_wallpaper_file(self):
        """ Set this attribute to its fallback value. """
        if self.thunderbird_num:
            filename = f"wallpaper_t{self.thunderbird_num}.png"
        else:
            filename = "default.jpg"
        self.path_to_wallpaper_file = \
            str(Path(PATH_TO_DEFAULT_WALLPAPER_DIR)/filename)

    @classmethod
    def read(cls) -> Self:
        """ Create an instance of this class by reading the config file. """
        with open(PATH_TO_HMSS_CONFIG, "r") as config_file:
            init_dict = json.load(config_file)
        result = cls(**init_dict)
        return result

    @classmethod
    def read_machine(cls) -> Self:
        """ A machine-interface version of the read() method. """
        return cls.read()

    @classmethod
    def read_human(cls) -> Self|None:
        """ A human-interface version of the read() method. """
        if not Path(PATH_TO_HMSS_CONFIG).exists():
            print("Looks like you don't have an HMSS config file.")
            print(f"I'll create one for you now at {PATH_TO_HMSS_CONFIG}")
            cls.write_defaults()
            print("Presently, all configs are set to their default values.")
            print("Open the file, amened as required, and then run me again.")
            return None
        try:
            result = cls.read()
        except TypeError:
            print("Looks like there's something wrong with your config file.")
            print(f"Path to your config file: {PATH_TO_HMSS_CONFIG}")
            print("For reference, this is the default config file:")
            print(DEFAULT_HMSS_CONFIG)
            return None
        return result

    @staticmethod
    def write_defaults(overwrite: bool = False):
        """ Create the config file, as necessary. """
        if overwrite or not Path(PATH_TO_HMSS_CONFIG).exists():
            with open(PATH_TO_HMSS_CONFIG, "w") as config_file:
                json.dump(DEFAULT_HMSS_CONFIG, config_file, indent=JSON_INDENT)
