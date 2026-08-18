"""Tests for dependency installation helpers."""

from subprocess import CalledProcessError
from unittest.mock import call, patch

from source.install_dependencies import (
    install_apt_package,
    install_apt_packages,
    install_dependencies,
    install_dependency,
)


@patch("source.install_dependencies.subprocess.run")
def test_install_dependency(run_mock):
    """Pip installation reports subprocess success and failure."""
    assert install_dependency("example>=1")
    run_mock.assert_called_once_with(
        ["pip", "install", "example>=1"], check=True
    )

    run_mock.side_effect = CalledProcessError(1, "pip")
    assert not install_dependency("example>=1")


@patch("source.install_dependencies.install_dependency")
def test_install_dependencies_stops_at_first_failure(install_mock):
    """A batch stops rather than concealing a failed package."""
    install_mock.side_effect = [True, False]

    assert not install_dependencies(["one", "two", "three"])
    assert install_mock.call_args_list == [call("one"), call("two")]


@patch("source.install_dependencies.subprocess.run")
def test_install_apt_package(run_mock):
    """APT arguments and non-raising failure behaviour are respected."""
    assert install_apt_package("example", quiet=True)
    run_mock.assert_called_once_with(
        ["sudo", "apt-get", "install", "--yes", "example"], check=True
    )

    run_mock.side_effect = CalledProcessError(1, "apt-get")
    assert not install_apt_package("example", raise_error=False, quiet=True)


@patch("source.install_dependencies.install_apt_package")
def test_install_apt_packages_is_quiet_per_package(install_mock):
    """The batch-level notice is not repeated for every package."""
    install_mock.return_value = True

    assert install_apt_packages(["one", "two"], quiet=True)
    assert install_mock.call_args_list == [
        call("one", quiet=True),
        call("two", quiet=True),
    ]
