"""Console entry points for Hosker Utils."""

from pathlib import Path

from .hm_software_installer import install_hmss
from .royal_repos_backup import back_up_royal_repos

BASHRC_ADDITION = "back-up-royal-repos &>/dev/null & disown"
PATH_TO_BASHRC = Path.home()/".bashrc"


def back_up_royal_repos_cli() -> int:
    """Back up the configured repositories and return a shell exit code."""
    return 0 if back_up_royal_repos() else 1


def install_hmss_cli() -> int:
    """Run the interactive HMSS installer and return a shell exit code."""
    return 0 if install_hmss(human_interface=True) else 1


def schedule_backup_cli() -> int:
    """Add the repository-backup command to the user's shell startup file."""
    existing = PATH_TO_BASHRC.read_text(encoding="utf-8") \
        if PATH_TO_BASHRC.exists() else ""
    if BASHRC_ADDITION in existing:
        print("Looks like the bashrc addition is there already.")
        return 0

    separator = "" if not existing or existing.endswith("\n") else "\n"
    with PATH_TO_BASHRC.open("a", encoding="utf-8") as bashrc:
        bashrc.write(f"{separator}{BASHRC_ADDITION}\n")
    return 0

