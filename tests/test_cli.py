"""Tests for the installed command entry points."""

from unittest.mock import patch

from source.cli import (
    BASHRC_ADDITION,
    back_up_royal_repos_cli,
    install_hmss_cli,
    schedule_backup_cli,
)


@patch("source.cli.back_up_royal_repos")
def test_backup_exit_code(backup_mock):
    """The backup command exposes success and failure to the shell."""
    backup_mock.side_effect = [True, False]
    assert back_up_royal_repos_cli() == 0
    assert back_up_royal_repos_cli() == 1


@patch("source.cli.install_hmss")
def test_installer_exit_code(installer_mock):
    """The installer command exposes success and failure to the shell."""
    installer_mock.side_effect = [True, False]
    assert install_hmss_cli() == 0
    assert install_hmss_cli() == 1
    installer_mock.assert_called_with(human_interface=True)


def test_schedule_backup(tmp_path):
    """Scheduling is idempotent and preserves the preceding final line."""
    bashrc_path = tmp_path/".bashrc"
    bashrc_path.write_text("existing command", encoding="utf-8")

    with patch("source.cli.PATH_TO_BASHRC", bashrc_path):
        assert schedule_backup_cli() == 0
        assert schedule_backup_cli() == 0

    assert bashrc_path.read_text(encoding="utf-8") == (
        f"existing command\n{BASHRC_ADDITION}\n"
    )
