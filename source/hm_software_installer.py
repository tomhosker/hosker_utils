"""
This code defines a class which installs the various packages and repositories
required on this computer.
"""

# Standard imports.
import subprocess
from dataclasses import dataclass
from pathlib import Path

# Local imports.
from .hmss_config import HMSSConfig

##############
# MAIN CLASS #
##############

def install_hmss(*args, **kwargs) -> bool:
    """Compress the class into a function."""
    installer_obj = HMSoftwareInstaller(*args, **kwargs)
    return installer_obj.run()


@dataclass
class HMSoftwareInstaller:
    """The class in question."""
    human_interface: bool = False
    config: HMSSConfig | None = None

    def __post_init__(self):
        if not self.config:
            if self.human_interface:
                self.config = HMSSConfig.read_human()
            else:
                self.config = HMSSConfig.read_machine()

    def _run_command(
        self,
        command: list[str],
        cwd: Path | None = None
    ) -> bool:
        """Run a command and report success."""
        try:
            subprocess.run(command, check=True, cwd=cwd)
        except subprocess.CalledProcessError:
            return False
        return True

    def _request_sudo(self) -> bool:
        """Ask for superuser privileges up front."""
        print("I'm going to need superuser privileges to install HMSS...")
        return self._run_command(["sudo", "-v"])

    def _install_apt_packages(self, packages: list[str] | None, label: str) -> bool:
        """Install a package list with APT."""
        if not packages:
            print(f"No {label} APT packages to install.")
            return True
        return self._run_command(
            ["sudo", "apt", "install", "--yes", *packages]
        )

    def _clone_royal_repo(self, repo_name: str, git_url_stem: str) -> bool:
        """Clone a single royal repo if it is not already present."""
        path_to_repo = Path.home() / repo_name
        if path_to_repo.exists():
            print(f"Looks like we've already got {repo_name}...")
            return True
        return self._run_command(
            ["git", "clone", f"{git_url_stem}/{repo_name}"],
            cwd=Path.home()
        )

    def _clone_royal_repos(self, git_url_stem: str) -> bool:
        """Clone all configured royal repos."""
        for repo_name in self.config.royal_repos or []:
            if not self._clone_royal_repo(repo_name, git_url_stem):
                return False
        return True

    def _schedule_backups(self) -> bool:
        """Install the shell hook that backs up royal repos on shell start."""
        if not self.config.royal_repos:
            return True
        return self._run_command(["schedule-back-up-royal-repos"])

    def _set_wallpaper(self) -> bool:
        """Set the GNOME wallpaper."""
        wallpaper_uri = Path(self.config.path_to_wallpaper_file).as_uri()
        return self._run_command(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                wallpaper_uri
            ]
        )

    def _get_git_url_stem(self) -> str | None:
        """Build the SSH Git URL stem from config."""
        if self.config.clone_method == "ssh":
            return f"git@{self.config.git_host}:{self.config.git_account_name}"
        print(f"Bad CLONE_METHOD: {self.config.clone_method}")
        return None

    def run(self) -> bool:
        """Run the installation routine."""
        if not self.config:
            return False
        if not self._request_sudo():
            return False
        if not self._run_command(["sudo", "apt", "update"]):
            return False
        if not self._run_command(["sudo", "apt", "upgrade", "--yes"]):
            return False
        if not self._install_apt_packages(
            self.config.essential_apt_packages,
            "essential"
        ):
            return False
        if not self._install_apt_packages(
            self.config.non_essential_apt_packages,
            "non-essential"
        ):
            return False
        git_url_stem = self._get_git_url_stem()
        if not git_url_stem:
            return False
        if not self._clone_royal_repos(git_url_stem):
            return False
        if not self._schedule_backups():
            return False
        if not self._set_wallpaper():
            return False
        print("All good. :)")
        return True
