#!/bin/sh

# Crash on errors and unset variables.
set -eu

RELEASE_ENV=".venv-release"
RELEASE_PYTHON="$RELEASE_ENV/bin/python"

# Keep release tooling isolated from both the system Python and the package's
# runtime environment.
if [ ! -x "$RELEASE_PYTHON" ]; then
    python3 -m venv "$RELEASE_ENV"
fi
"$RELEASE_PYTHON" -m pip install --upgrade build twine

# Build and validate release artifacts. Publishing is deliberately separate so
# running this script cannot upload a package by accident.
"$RELEASE_PYTHON" -m build
"$RELEASE_PYTHON" -m twine check dist/*

echo "Artifacts are ready in dist/."
echo "Publish with: $RELEASE_PYTHON -m twine upload dist/*"
