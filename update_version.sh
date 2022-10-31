#!/bin/sh

# Crash on the first error.
set -e

# Check/install twine.
sudo apt install --yes twine

# Let's get cracking...
echo "This may fail if you've not updated the version number in setup.py."
python3 setup.py check
python3 setup.py sdist
python3 setup.py bdist_wheel
#twine upload --repository-url https://test.pypi.org/legacy/ dist/* # This is for uploading to test.pypi.
twine upload dist/* --verbose
