"""
This code defines some useful functions when writing a minimal continuous
integration routine.
"""

# Standard imports.
import shutil
import subprocess
import sys
from pathlib import Path

# Non-standard imports.
from termcolor import colored

DEFAULT_PATH_TO_LINTER_RC = "ruff.toml"
PATH_TO_BACKUP_LINTER_RC = \
    str(Path(__file__).parent/"backup_configs"/"backup_ruff.toml")
DEFAULT_PATH_TO_TEST_INI = "pytest.ini"
PATH_TO_BACKUP_TEST_INI = \
    str(Path(__file__).parent/"backup_configs"/"backup_pytest.ini")
PIP_INSTALL_THIS = ("pip", "install", ".")
BUNDLED_RUFF_PATH = Path("/usr/lib/hosker-utils/ruff")

#############
# FUNCTIONS #
#############

def print_encased(message, symbol="#", colour=None):
    """ Print the message encased in hashes. """
    message_line = symbol+" "+message+" "+symbol
    hashes = ""
    for _ in range(len(message_line)):
        hashes = hashes+symbol
    if colour:
        print(colored(" ", colour))
        print(colored(hashes, colour))
        print(colored(message_line, colour))
        print(colored(hashes, colour))
        print(colored(" ", colour))
    else:
        print(" ")
        print(hashes)
        print(message_line)
        print(hashes)
        print(" ")
    sys.stdout.flush()

def run_tests(path_to_test_ini=DEFAULT_PATH_TO_TEST_INI):
    """ Run PyTest. """
    if not Path(path_to_test_ini).exists():
        shutil.copy(PATH_TO_BACKUP_TEST_INI, path_to_test_ini)
    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "-c", path_to_test_ini],
            check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return False
    return True

def run_linter(path_to_linter_rc=DEFAULT_PATH_TO_LINTER_RC):
    """Run Ruff on this repo."""
    if not Path(path_to_linter_rc).exists():
        shutil.copy(PATH_TO_BACKUP_LINTER_RC, path_to_linter_rc)
    ruff_command = shutil.which("ruff")
    if BUNDLED_RUFF_PATH.exists():
        ruff_command = str(BUNDLED_RUFF_PATH)
    command = (
        [ruff_command]
        if ruff_command
        else [sys.executable, "-m", "ruff"]
    )
    arguments = command + [
        "check",
        "--quiet",
        "--config",
        path_to_linter_rc,
        ".",
    ]
    try:
        subprocess.run(arguments, check=True)
    except (OSError, subprocess.CalledProcessError):
        return False
    return True

def run_continuous_integration_no_print(
        lint=True, test=True, stop_on_failure=False
    ):
    """ Execute a minimal continuous integration routine. """
    lint_result, test_result = True, True
    if lint:
        lint_result = run_linter()
        if (not lint_result) and stop_on_failure:
            return False
    if test:
        test_result = run_tests()
        if (not test_result) and stop_on_failure:
            return False
    return bool(lint_result and test_result)

def run_continuous_integration(lint=True, test=True, stop_on_failure=False):
    """ Run this file. """
    print_encased("Starting continuous integration routine...")
    result = \
        run_continuous_integration_no_print(
            lint=lint, test=test, stop_on_failure=stop_on_failure
        )
    if result:
        print_encased("Continuous integration: PASS", colour="green")
    else:
        print_encased("Continuous integration: FAIL", colour="red")
    return result
