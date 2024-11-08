"""
This code gives us, amongst other things, the ability to import specific
classes and functions from the package directly, rather than having to go
through the modules in which they are defined.
"""

# Local imports.
from .continuous_integration import run_continuous_integration
from .hm_software_installer import HMSoftwareInstaller, PATH_TO_HMSS_CONFIG
from .install_dependencies import (
    install_dependency,
    install_dependencies,
    install_apt_package,
    install_apt_packages
)
from .local_utils import get_yes_no

######################
# FRONTEND UTILITIES #
######################

def install_hmss():
    """ Attempt to install His Majesty's Software Suite. """
    try:
        installer = HMSoftwareInstaller.read()
    except FileNotFoundError:
        print("Looks like you don't have an HMSS config file.")
        print(f"I'll to create for you now at {PATH_TO_HMSS_CONFIG}")
        HMSoftwareInstaller.write_defaults()
        print("Right now, all configs are set to their default values.")
        print("Open the file, amened as required, and then run me again.")
    else:
        installer.run()
