"""
This code defines a class which backs up the so-called royal repos.
"""

# Standard imports.
import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

# Local imports.
from .hmss_config import HMSSConfig

# Local constants.
PATH_TO_LOG = str(Path.home()/"hm_git.log")
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

##############
# MAIN CLASS #
##############

def back_up_royal_repos(*args, **kwargs) -> bool:
    """ Compress the class into a function. """
    backup_obj = RoyalRepoBackup(*args, **kwargs)
    return backup_obj.back_up_all()

@dataclass
class RoyalRepoBackup:
    human_interface: bool = False
    config: HMSSConfig = None
    logger: logging.Logger = field(init=False, default=None)

    def __post_init__(self):
        if not self.config:
            self._auto_set_config()
        self._auto_set_logger()

    def _auto_set_config(self):
        """ Ronseal. """
        if self.human_interface:
            self.config = HMSSConfig.read_human()
        else:
            self.config = HMSSConfig.read_machine()

    def _auto_set_logger(self):
        """ Construct our logging object. """
        result = logging.getLogger()
        result.setLevel(logging.INFO)
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler = logging.FileHandler(PATH_TO_LOG)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        result.addHandler(file_handler)
        self.logger = result

    def _fetch_royal(self, path_to: str) -> bool:
        """ Run `git fetch` on a given repo. """
        return self._run_git_command("fetch", path_to)

    def _pull_royal(self, path_to: str) -> bool:
        """ Run `git pull` on a given repo. """
        return self._run_git_command("pull", path_to)

    def _run_git_command(self, command: str, git_directory: str) -> bool:
        """ Run a given Git command in a given Git directory. """
        try:
            subprocess.run(["git", command], check=True, cwd=git_directory)
        except CalledProcessError as exc:
            self.logger.error(
                "Non-zero exit code running git %s within %s: %s",
                command,
                git_directory,
                format(exc)
            )
            return False
        return True

    def back_up_all(self) -> bool:
        """ Back up ALL royal repos. """
        result = True
        self.logger.info("Backing up royal repos...")
        for repo in self.config.royal_repos:
            if not self.back_up_one(repo):
                result = False
        if result:
            self.logger.info("Backed up royal repos successfully.")
        else:
            self.logger.error("Error backing up royal repos.")
        return result

    def back_up_one(self, repo_name: str) -> bool:
        """ Back up a given INDIVIDUAL royal repo. """
        path_to = str(Path.home()/repo_name)
        if not (
            self._fetch_royal(path_to) and
            self._pull_royal(path_to)
        ):
            self.logger.error("Error backing up: %s", repo_name)
            return False
        return True
