"""
This code tests the RoyalRoyalReposBackup class.
"""

# Standard imports.
from pathlib import Path
from unittest.mock import Mock, patch

# Source imports.
from source.royal_repos_backup import RoyalReposBackup

# Local constants.
TEST_PATH_TO_HMSS_CONFIG = "test_hmss_config.json"
TEST_PATH_TO_LOG = "test.log"

###########
# TESTING #
###########

@patch("source.hmss_config.PATH_TO_HMSS_CONFIG", TEST_PATH_TO_HMSS_CONFIG)
@patch("source.royal_repos_backup.PATH_TO_LOG", TEST_PATH_TO_LOG)
def test_royal_repos_backup():
    """ Test that the class works as intended. """
    Path(TEST_PATH_TO_HMSS_CONFIG).unlink(missing_ok=True)
    Path(TEST_PATH_TO_LOG).unlink(missing_ok=True)
    backup_obj = RoyalReposBackup(human_interface=True)
    backup_obj = RoyalReposBackup()
    backup_obj._run_git_command = Mock(return_value=True)
    backup_obj.back_up_all()
    Path(TEST_PATH_TO_HMSS_CONFIG).unlink()
    Path(TEST_PATH_TO_LOG).unlink()
