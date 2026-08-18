# Hosker Utils

This repository provides the `hosker_utils` Python package and command-line
helpers for configuring His Majesty's Software Suite (HMSS) and backing up a
configured set of Git repositories.

It also serves as a small, working reference for the standards expected in the
owner's other repositories: declarative packaging, isolated tests, one-command
validation, explicit release versions, and documented system effects. It is a
role model, not a template; copy the principles rather than every file.

## Requirements

- Python 3.11 or newer
- A Debian-based Linux distribution for the HMSS installer

## Development

Create a virtual environment, install the package, and run the checks:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m ruff check .
.venv/bin/python -m pytest
.venv/bin/python validate.py
```

The installer runs `apt` through `sudo`, changes the GNOME wallpaper, and
clones the repositories listed in `~/hmss_config.json`. Review that generated
configuration before running the installer.

Build and validate Python release artifacts with `./update_version.sh`. The
script creates an ignored `.venv-release` environment and installs current
versions of `build` and Twine there; it never installs them into the system
Python. It writes only PyPI-compatible artifacts to `dist/python/`, keeping
them separate from Debian packages. Before completing a pull request, agree
and set the next version in `pyproject.toml`.

Building and `twine check` are local operations. Only the separate
`twine upload` release step contacts PyPI; the script prints that command but
does not run it automatically.

For a release-affecting change, the final checklist is:

1. Run `python3 validate.py` and `git diff --check`.
2. Agree and update the version in `pyproject.toml`.
3. Build and validate the Python wheel and source distribution.
4. Build and inspect the Debian package when Debian packaging has changed.
5. Publish only as a separate, deliberate action.

## Install

For an isolated command-line installation on any supported distribution, use
`pipx`:

```sh
pipx install .
```

On Debian-based systems, build and install a native package instead:

```sh
python3 tools/build_deb.py
sudo apt install ./dist/hosker-utils_2.7.0_$(dpkg --print-architecture).deb
```

The Debian builder requires `dpkg-deb`, stages files in a temporary directory,
and does not require root. APT handles the package's Python runtime
dependencies. Because Ruff is not available in all APT catalogues, the builder
bundles the Ruff executable from the active development environment.

## Install HMSS

After installing by either method, run `install-hmss`.
