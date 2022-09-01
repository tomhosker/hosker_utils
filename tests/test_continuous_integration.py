"""
This code tests some of the continuous integration functions.
"""

# Source imports.
from source.continuous_integration import print_encased

###########
# TESTING #
###########

def test_print_encased():
    """ Test that the function runs without crashing. """
    print_encased("Some random guff.")
