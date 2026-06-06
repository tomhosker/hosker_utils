"""
This code tests the HMSSConfig class.
"""

# Standard imports.
from pathlib import Path
from unittest.mock import patch

# Source imports.
from source.hm_software_installer import HMSoftwareInstaller

# Local constants.
TEST_PATH_TO_HMSS_CONFIG = "test_hmss_config.json"

###########
# TESTING #
###########

@patch("source.hmss_config.PATH_TO_HMSS_CONFIG", TEST_PATH_TO_HMSS_CONFIG)
@patch("source.hm_software_installer.subprocess.run")
def test_hm_software_installer(mock_run):
    """ Test that the class works as intended. """
    Path(TEST_PATH_TO_HMSS_CONFIG).unlink(missing_ok=True)
    installer_obj = HMSoftwareInstaller(human_interface=True)
    assert not installer_obj.run()
    installer_obj = HMSoftwareInstaller()
    assert installer_obj.run()
    assert mock_run.called
    Path(TEST_PATH_TO_HMSS_CONFIG).unlink()
