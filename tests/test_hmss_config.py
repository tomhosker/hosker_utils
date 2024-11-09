"""
This code tests the HMSSConfig class.
"""

# Standard imports.
from pathlib import Path
from unittest.mock import patch

# Source imports.
from source.hmss_config import HMSSConfig, DEFAULT_HMSS_CONFIG

# Local constants.
TEST_PATH_TO_HMSS_CONFIG = "test_hmss_config.json"

###########
# TESTING #
###########

@patch("source.hmss_config.PATH_TO_HMSS_CONFIG", TEST_PATH_TO_HMSS_CONFIG)
def test_hmss_config():
    """ Test that the class works as intended. """
    Path(TEST_PATH_TO_HMSS_CONFIG).unlink(missing_ok=True)
    assert HMSSConfig.read_human() == None
    config_obj = HMSSConfig.read_machine()
    for key, value in DEFAULT_HMSS_CONFIG.items():
        if key != "path_to_wallpaper_file":
            assert value == getattr(config_obj, key)
    Path(TEST_PATH_TO_HMSS_CONFIG).unlink()
