# Hosker Utils

This repository provides the `hosker_utils` Python package and command-line
helpers for configuring His Majesty's Software Suite (HMSS) and backing up a
configured set of Git repositories.

## Requirements

- Python 3.11 or newer
- A Debian-based Linux distribution for the HMSS installer

## Development

Create a virtual environment, install the package, and run the checks:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m ruff check .
.venv/bin/python -m pytest
.venv/bin/python validate.py
```

The installer runs `apt` through `sudo`, changes the GNOME wallpaper, and
clones the repositories listed in `~/hmss_config.json`. Review that generated
configuration before running the installer.

Build release artifacts with `python3 -m build`. Validate them with
`python3 -m twine check dist/*` before publishing.

## Install HMSS

To install His Majesty's Software Suite:

1. Run `python3 -m pip install --user .` in this directory.
2. Run `install-hmss`.

On distributions that prevent system Python package installation, use a
virtual environment or `pipx` instead of overriding the package manager.
