"""
This code defines a class which installs the various packages and repositories
required on this computer.
"""

# Standard imports.
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

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
PATH_TO_INSTALL_SCRIPT_BASE = str(PATH_OBJ_TO_HERE/"sh"/"install_hmss_base.sh")
PATH_TO_INSTALL_SCRIPT_TEMP = str(Path.home()/"install_hmss_temp.sh")
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
class HMSoftwareInstaller:
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

    def _write_install_script(self):
        """ Read the base file; make the replacements; write the new file. """
        with open(PATH_TO_INSTALL_SCRIPT_BASE, "r") as base_file:
            script = base_file.read()
        replacements = (
            ("%ESSENTIAL_APT_PACKAGES%", sh_list(self.essential_apt_packages)),
            ("%INSTALL_CHROME%", sh_bool(self.install_chrome)),
            (
                "%NON_ESSENTIAL_APT_PACKAGES%",
                sh_list(self.non_essential_apt_packages)
            ),
            ("%ROYAL_REPOS%", sh_list(self.royal_repos)),
            ("%CLONE_METHOD%", self.clone_method),
            ("%GIT_HOST%", self.git_host),
            ("%GIT_ACCOUNT_NAME%", self.git_account_name),
            ("%PATH_TO_WALLPAPER%", self.path_to_wallpaper_file)
        )
        for pair in replacements:
            script = script.replace(*pair)
        with open(PATH_TO_INSTALL_SCRIPT_TEMP, "w") as temp_file:
            temp_file.write(script)

    def _run_install_script(self) -> bool:
        """ Ronseal. """
        try:
            subprocess.run(["sh", PATH_TO_INSTALL_SCRIPT_TEMP], check=True)
        except subprocess.CalledProcessError:
            return False
        return True

    def _clean(self):
        """ Remove any temporary files which have served their purpose. """
        Path(PATH_TO_INSTALL_SCRIPT_TEMP).unlink(missing_ok=True)

    def run(self):
        """ Run the installation routine. """
        self._write_install_script()
        if self._run_install_script():
            self._clean()

    @classmethod
    def read(cls):
        """ Create an instance of this class by reading the config file. """
        with open(PATH_TO_HMSS_CONFIG, "r") as config_file:
            init_dict = json.load(config_file)
        result = cls(**init_dict)
        return result

    @staticmethod
    def write_defaults(overwrite: bool = False):
        """ Create the config file, as necessary. """
        if overwrite or not Path(PATH_TO_HMSS_CONFIG).exists():
            with open(PATH_TO_HMSS_CONFIG, "w") as config_file:
                json.dump(DEFAULT_HMSS_CONFIG, config_file, indent=JSON_INDENT)

################################
# HELPER CLASSES AND FUNCTIONS #
################################

class HMSSError(Exception):
    """ A custom exception. """

def sh_bool(py_bool: bool) -> str:
    """
    Convert a Python boolean to its string representation in Shell Script.
    """
    if py_bool is True:
        return "true"
    elif py_bool is False:
        return "false"
    else:
        raise HMSSError(f"Not a boolean: {py_bool}")

def sh_list(py_list: list|None) -> str:
    """ Convert a Python list to its string representation in Shell Script. """
    if py_list is None:
        return ""
    result = " ".join(py_list)
    return result
