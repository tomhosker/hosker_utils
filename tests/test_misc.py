"""
This code tests some of the miscellaneous functions.
"""

# Standard imports.
from unittest.mock import patch

# Source imports.
from source.misc import get_yes_no

###########
# TESTING #
###########

@patch("source.misc.input")
def test_get_yes_no(input_mock):
    """ Test that "y" returns True and "n" returns False. """
    input_mock.return_value = "y"
    assert get_yes_no("message")
    input_mock.return_value = "n"
    assert not get_yes_no("message")
