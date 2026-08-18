"""
This code tests the HMSSConfig class.
"""

# Standard imports.
from unittest.mock import patch

# Source imports.
from source.hmss_config import DEFAULT_HMSS_CONFIG, HMSSConfig

###########
# TESTING #
###########

def test_hmss_config(tmp_path):
    """ Test that the class works as intended. """
    config_path = tmp_path/"hmss_config.json"
    with patch("source.hmss_config.PATH_TO_HMSS_CONFIG", str(config_path)):
        assert HMSSConfig.read_human() is None
        config_obj = HMSSConfig.read_machine()
        for key, value in DEFAULT_HMSS_CONFIG.items():
            if key != "path_to_wallpaper_file":
                assert value == getattr(config_obj, key)
