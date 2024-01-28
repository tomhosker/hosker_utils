"""
This file lists some configurations for HMSS.
"""

# Standard imports.
from pathlib import Path

##################
# CONFIGURATIONS #
##################

# Components.
PATH_OBJ_TO_HOME = Path.home()

# Defaults.
DEFAULT_BRANCH_NAME = "master"
DEFAULT_EMAIL_ADDRESS = "tomdothosker@gmail.com"
DEFAULT_ENCODING = "utf-8"
DEFAULT_GIT_USERNAME = "tomhosker"
DEFAULT_PLATFORM = "ubuntu"
DEFAULT_PYTHON_VERSION = 3
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
DEFAULT_TARGET_DIR = str(PATH_OBJ_TO_HOME)
DEFAULT_WALLPAPER_FN = "default.jpg"
# Default paths.
DEFAULT_PATH_TO_HMSS_CONFIG_FILE = str(PATH_OBJ_TO_HOME/"hmss_config.json")
DEFAULT_PATH_TO_GIT_CREDENTIALS = str(PATH_OBJ_TO_HOME/".git-credentials")
DEFAULT_PATH_TO_PAT = str(PATH_OBJ_TO_HOME/"personal_access_token.txt")
DEFAULT_PATH_TO_WALLPAPER_DIR = str(Path(__file__).parent/"wallpaper")

# Operating systems.
UBUNTU = "ubuntu"
CHROME_OS = "chrome-os"
RASPBIAN = "raspian"
OTHER_DEBIAN = "other-debian"

# Action components.
IMPERATIVE = "imperative"
GERUND = "gerund"
METHOD = "method"

# Misc.
CODE_INDENTATION = 4
GIT = "git"
INTERNAL_PYTHON_COMMAND = "python3"
