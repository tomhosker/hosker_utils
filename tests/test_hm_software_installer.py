"""
This code tests the HMSSConfig class.
"""

# Standard imports.
from unittest.mock import patch

# Source imports.
from source.hm_software_installer import HMSoftwareInstaller

###########
# TESTING #
###########

def test_hm_software_installer(tmp_path):
    """ Test that the class works as intended. """
    config_path = tmp_path/"hmss_config.json"
    script_path = tmp_path/"install_hmss_temp.sh"
    with (
        patch("source.hmss_config.PATH_TO_HMSS_CONFIG", str(config_path)),
        patch(
            "source.hm_software_installer.PATH_TO_INSTALL_SCRIPT_TEMP",
            str(script_path)
        )
    ):
        installer_obj = HMSoftwareInstaller(human_interface=True)
        assert not installer_obj.run()

        installer_obj = HMSoftwareInstaller()
        with patch.object(
            HMSoftwareInstaller, "_run_install_script", return_value=True
        ):
            assert installer_obj.run()
        assert not script_path.exists()

        with patch.object(
            HMSoftwareInstaller, "_run_install_script", return_value=False
        ):
            assert not installer_obj.run()
        assert not script_path.exists()
