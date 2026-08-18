"""Tests for native Debian package construction."""

import subprocess

from tools.build_deb import build_deb, get_architecture, read_configuration


def test_deb_configuration_uses_project_version():
    """The Debian builder has no independent version to become stale."""
    project, scripts, deb = read_configuration()

    assert project["version"] == "2.7.0"
    assert deb["package-name"] == "hosker-utils"
    assert set(scripts) == {
        "back-up-royal-repos",
        "install-hmss",
        "schedule-back-up-royal-repos",
    }


def test_build_deb(tmp_path):
    """The artifact contains package modules and executable commands."""
    fake_ruff = tmp_path/"bin/ruff"
    fake_ruff.parent.mkdir()
    fake_ruff.write_text("#!/bin/sh\n", encoding="utf-8")
    ruff_license_dir = tmp_path/"ruff-1.0.dist-info/licenses"
    ruff_license_dir.mkdir(parents=True)
    (ruff_license_dir/"LICENSE").write_text("MIT", encoding="utf-8")
    output_path = build_deb(tmp_path, fake_ruff)
    contents = subprocess.run(
        ["dpkg-deb", "--contents", str(output_path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    assert output_path.name == (
        f"hosker-utils_2.7.0_{get_architecture()}.deb"
    )
    assert "./usr/lib/python3/dist-packages/hosker_utils/cli.py" in contents
    assert "./usr/bin/install-hmss" in contents
    assert "./usr/lib/hosker-utils/ruff" in contents
    assert "./usr/share/doc/hosker-utils/ruff-copyright" in contents
    assert "./usr/share/doc/hosker-utils/copyright" in contents
    install_line = next(
        line
        for line in contents.splitlines()
        if "./usr/bin/install-hmss" in line
    )
    assert "-rwxr-xr-x root/root" in install_line
