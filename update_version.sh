#!/bin/sh

# Crash on errors and unset variables.
set -eu

RELEASE_ENV=".venv-release"
RELEASE_PYTHON="$RELEASE_ENV/bin/python"
RELEASE_OUTPUT_DIR="dist/python"

# Keep release tooling isolated from both the system Python and the package's
# runtime environment.
if [ ! -x "$RELEASE_PYTHON" ]; then
    python3 -m venv "$RELEASE_ENV"
fi
"$RELEASE_PYTHON" -m pip install --upgrade build twine

# Build and validate release artifacts. Publishing is deliberately separate so
# running this script cannot upload a package by accident.
rm -rf "$RELEASE_OUTPUT_DIR"
"$RELEASE_PYTHON" -m build --outdir "$RELEASE_OUTPUT_DIR"
"$RELEASE_PYTHON" -m twine check "$RELEASE_OUTPUT_DIR"/*

echo "Python artifacts are ready in $RELEASE_OUTPUT_DIR/."
echo "Publish with: $RELEASE_PYTHON -m twine upload $RELEASE_OUTPUT_DIR/*"
