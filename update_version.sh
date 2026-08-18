#!/bin/sh

# Crash on the first error.
set -e

# Build and validate release artifacts. Publishing is deliberately separate so
# running this script cannot upload a package by accident.
python3 -m build
python3 -m twine check dist/*

echo "Artifacts are ready in dist/. Publish with: python3 -m twine upload dist/*"
