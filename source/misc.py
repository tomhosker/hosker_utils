"""
This code defines some utility functions and constants used across this project.
"""

# Constants.
GIT = "git"

#############
# FUNCTIONS #
#############

def get_yes_no(message: str) -> bool:
    """ Get the user to answer a yes/no question. """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    print(message+" [y/n]")
    answer = input().lower()
    if answer in valid:
        return valid[answer]
    return False
