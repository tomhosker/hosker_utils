"""
This code defines a class which installs the various packages and repositories
required on this computer.
"""

# Standard imports.
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

# Local imports.
from .hmss_config import HMSSConfig

# Local constants.
PATH_OBJ_TO_HERE = Path(__file__).parent
PATH_TO_INSTALL_SCRIPT_BASE = str(PATH_OBJ_TO_HERE/"sh"/"install_hmss_base.sh")
PATH_TO_INSTALL_SCRIPT_TEMP = str(Path.home()/"install_hmss_temp.sh")

##############
# MAIN CLASS #
##############

def install_hmss(*args, **kwargs) -> bool:
    """ Compress the class into a function. """
    installer_obj = HMSoftwareInstaller(*args, **kwargs)
    return installer_obj.run()

@dataclass
class HMSoftwareInstaller:
    """ The class in question. """
    human_interface: bool = False
    config: HMSSConfig|None = None

    def __post_init__(self):
        if not self.config:
            if self.human_interface:
                self.config = HMSSConfig.read_human()
            else:
                self.config = HMSSConfig.read_machine()

    def _write_install_script(self):
        """ Read the base file; make the replacements; write the new file. """
        with open(PATH_TO_INSTALL_SCRIPT_BASE, "r") as base_file:
            script = base_file.read()
        replacements = (
            (
                "%ESSENTIAL_APT_PACKAGES%",
                sh_list(self.config.essential_apt_packages)
            ), (
                "%INSTALL_CHROME%",
                sh_bool(self.config.install_chrome)
            ), (
                "%NON_ESSENTIAL_APT_PACKAGES%",
                sh_list(self.config.non_essential_apt_packages)
            ), (
                "%ROYAL_REPOS%",
                sh_list(self.config.royal_repos)
            ), (
                "%CLONE_METHOD%",
                self.config.clone_method
            ), (
                "%GIT_HOST%",
                self.config.git_host
            ), (
                "%GIT_ACCOUNT_NAME%",
                self.config.git_account_name
            ), (
                "%PATH_TO_WALLPAPER%",
                self.config.path_to_wallpaper_file
            )
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
        if not self.config:
            return False
        self._write_install_script()
        if self._run_install_script():
            self._clean()
            return True
        return False

################################
# HELPER CLASSES AND FUNCTIONS #
################################

class HMSSError(Exception):
    """ A custom exception. """

def sh_bool(py_bool: bool) -> str:
    """ Convert a Python boolean to its Shell Script equivalent. """
    if py_bool is True:
        return "true"
    elif py_bool is False:
        return "false"
    else:
        raise HMSSError(f"Not a boolean: {py_bool}")

def sh_list(py_list: list|None) -> str:
    """ Convert a Python list to its Shell Script equivalent. """
    if not py_list:
        return ""
    result = " ".join(py_list)
    return result
