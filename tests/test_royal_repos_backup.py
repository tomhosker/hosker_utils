"""
This code tests the RoyalRoyalReposBackup class.
"""

# Standard imports.
from unittest.mock import patch

# Source imports.
from source.royal_repos_backup import RoyalReposBackup

###########
# TESTING #
###########

def test_royal_repos_backup(tmp_path):
    """ Test that the class works as intended. """
    config_path = tmp_path/"hmss_config.json"
    log_path = tmp_path/"hm_git.log"
    with (
        patch("source.hmss_config.PATH_TO_HMSS_CONFIG", str(config_path)),
        patch("source.royal_repos_backup.PATH_TO_LOG", str(log_path))
    ):
        assert not RoyalReposBackup(human_interface=True).back_up_all()
        backup_obj = RoyalReposBackup()
        with patch.object(
            RoyalReposBackup, "_run_git_command", return_value=True
        ):
            assert backup_obj.back_up_all()
