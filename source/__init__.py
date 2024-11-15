"""
This code gives us, amongst other things, the ability to import specific
classes and functions from the package directly, rather than having to go
through the modules in which they are defined.
"""

# Local imports.
from .continuous_integration import run_continuous_integration
from .hm_software_installer import HMSoftwareInstaller, install_hmss
from .install_dependencies import (
    install_dependency,
    install_dependencies,
    install_apt_package,
    install_apt_packages
)
from .misc import get_yes_no
