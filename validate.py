"""
This code defines a continuous integration routine for this repository.
"""

# Local imports.
from source.continuous_integration import run_continuous_integration

###################
# RUN AND WRAP UP #
###################

def run():
    """ Run this file. """
    run_continuous_integration()

if __name__ == "__main__":
    run()
