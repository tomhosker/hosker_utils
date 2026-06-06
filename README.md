# Hosker Utils

This repository defines a PIP package defining some **utility functions** of
general application.

## Install HMSS

To install His Majesty's Software Suite:

1. Run `pip install --break-system-packages .` in this directory.
1. Run `install-hmss`.

## Build A Debian Package

To build a minimal `.deb` file:

1. Run `scripts/build-deb`.
1. Install the resulting file with `sudo apt install ./dist/hosker-utils_2.6.1_all.deb`.
