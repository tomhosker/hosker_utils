"""
This code tests some of the continuous integration functions.
"""

# Source imports.
from source.continuous_integration import print_encased, run_linter

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
