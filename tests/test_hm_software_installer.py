"""
This code tests the HMSoftwareInstaller class.
"""

# Local imports.
from hm_software_installer import HMSoftwareInstaller

###########
# TESTING #
###########

def test_run():
    """ Carry out a test run with the object. """
    installer_obj = HMSoftwareInstaller(test_run=True)
    assert installer_obj.run()
