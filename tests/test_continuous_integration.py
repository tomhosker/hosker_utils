"""
This code tests some of the continuous integration functions.
"""

# Standard imports.
from unittest.mock import patch

# Source imports.
from source.continuous_integration import (
    print_encased,
    run_continuous_integration,
    run_continuous_integration_no_print,
    run_linter,
)

###########
# TESTING #
###########

def test_print_encased():
    """ Test that the function runs without crashing. """
    print_encased("Some random guff.")
    print_encased("Some random guff.", colour="orange")

def test_run_linter():
    """ Test that the function returns the right value. """
    assert run_linter()


@patch("source.continuous_integration.run_tests", return_value=True)
@patch("source.continuous_integration.run_linter", return_value=True)
def test_continuous_integration_passes(linter_mock, tests_mock):
    """The combined check passes when both underlying checks pass."""
    assert run_continuous_integration_no_print()
    linter_mock.assert_called_once_with()
    tests_mock.assert_called_once_with()


@patch("source.continuous_integration.run_tests", return_value=True)
@patch("source.continuous_integration.run_linter", return_value=False)
def test_continuous_integration_can_stop_after_lint_failure(
    linter_mock, tests_mock
):
    """Stop-on-failure avoids running tests after a lint failure."""
    assert not run_continuous_integration_no_print(stop_on_failure=True)
    linter_mock.assert_called_once_with()
    tests_mock.assert_not_called()


@patch("source.continuous_integration.run_tests", return_value=False)
@patch("source.continuous_integration.run_linter", return_value=True)
def test_continuous_integration_reports_test_failure(_linter_mock, _tests_mock):
    """A test failure propagates through the printing wrapper."""
    assert not run_continuous_integration(stop_on_failure=True)
