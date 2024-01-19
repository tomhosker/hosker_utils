#!/bin/sh

# Local constants.
PACKAGE_NAME="hosker_utils"

# Crash on the first error.
set -e

# Check/install twine.
echo "I'm going to need superuser privileges to check/install twine..."
sudo apt install --yes twine

# Let's get cracking...
rm -rf build dist "$PACKAGE_NAME.egg-info"
python3 setup.py check
python3 setup.py sdist
python3 setup.py bdist_wheel
#twine upload --repository-url https://test.pypi.org/legacy/ dist/* # This is for uploading to test.pypi.
if ! twine upload dist/* --verbose; then
    echo "Note to future Tom: Did you update the version number in setup.py?"
fi
