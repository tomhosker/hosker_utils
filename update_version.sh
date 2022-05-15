#!/bin/sh

set -e

echo "This may fail if you've not updated the version number in setup.py."

python3 setup.py check
python3 setup.py sdist
python3 setup.py bdist_wheel
#twine upload --repository-url https://test.pypi.org/legacy/ dist/* # This is for uploading to test.pypi.
twine upload dist/*
