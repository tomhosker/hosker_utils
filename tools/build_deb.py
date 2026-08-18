#!/usr/bin/env python3
"""Build a minimal Debian package without installing through pip."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_PATH = REPO_ROOT/"pyproject.toml"
SOURCE_DIR = REPO_ROOT/"source"
DEFAULT_OUTPUT_DIR = REPO_ROOT/"dist"


def read_configuration() -> tuple[dict, dict, dict]:
    """Return project, script-entry-point, and Debian configuration."""
    with PYPROJECT_PATH.open("rb") as pyproject_file:
        configuration = tomllib.load(pyproject_file)
    project = configuration["project"]
    return (
        project,
        project["scripts"],
        configuration["tool"]["hosker-utils"]["deb"],
    )


def write_control_file(
    debian_dir: Path,
    project: dict,
    deb: dict,
    architecture: str,
) -> None:
    """Write Debian control metadata derived from project configuration."""
    author = project["authors"][0]
    lines = [
        f"Package: {deb['package-name']}",
        f"Version: {project['version']}",
        f"Section: {deb['section']}",
        f"Priority: {deb['priority']}",
        f"Architecture: {architecture}",
        f"Maintainer: {author['name']} <{author['email']}>",
        f"Depends: {', '.join(deb['depends'])}",
        f"Description: {project['description']}",
        "",
    ]
    (debian_dir/"control").write_text("\n".join(lines), encoding="utf-8")


def copy_package(package_root: Path, scripts: dict[str, str]) -> None:
    """Copy Python sources and create wrappers for console entry points."""
    package_dir = package_root/"usr/lib/python3/dist-packages/hosker_utils"
    shutil.copytree(
        SOURCE_DIR,
        package_dir,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    bin_dir = package_root/"usr/bin"
    bin_dir.mkdir(parents=True)
    wrapper = """#!/usr/bin/python3
from {module} import {function}

raise SystemExit({function}())
"""
    for command, entry_point in scripts.items():
        module, function = entry_point.split(":", maxsplit=1)
        destination = bin_dir/command
        destination.write_text(
            wrapper.format(module=module, function=function),
            encoding="utf-8",
        )
        destination.chmod(0o755)

    documentation_dir = package_root/"usr/share/doc/hosker-utils"
    documentation_dir.mkdir(parents=True)
    shutil.copy2(REPO_ROOT/"LICENSE", documentation_dir/"copyright")


def normalize_permissions(package_root: Path) -> None:
    """Set conventional permissions on directories, commands, and data."""
    bin_dir = package_root/"usr/bin"
    for path in package_root.rglob("*"):
        if path.is_dir() or path.parent == bin_dir:
            path.chmod(0o755)
        else:
            path.chmod(0o644)


def find_ruff_binary(explicit_path: Path | None = None) -> Path:
    """Find the Ruff executable that will be bundled in the package."""
    candidates = [
        explicit_path,
        Path(sys.executable).parent/"ruff",
        Path(ruff_path) if (ruff_path := shutil.which("ruff")) else None,
    ]
    for candidate in candidates:
        if candidate and candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "Ruff is required to build the Debian package. Install the project "
        "in its development environment or pass --ruff-binary."
    )


def find_ruff_license(ruff_binary: Path) -> Path:
    """Find the licence shipped alongside a PyPI installation of Ruff."""
    search_root = ruff_binary.parent.parent
    licenses = search_root.glob("ruff-*.dist-info/licenses/LICENSE")
    if license_path := next(licenses, None):
        return license_path
    raise FileNotFoundError(
        "Could not find Ruff's licence beside its executable. Install Ruff "
        "from PyPI in the active environment before building."
    )


def get_architecture() -> str:
    """Return the architecture name used by Debian packages."""
    return subprocess.run(
        ["dpkg", "--print-architecture"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def build_deb(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    ruff_binary: Path | None = None,
) -> Path:
    """Build the Debian package and return the resulting path."""
    project, scripts, deb = read_configuration()
    architecture = get_architecture()
    ruff_binary = find_ruff_binary(ruff_binary)
    ruff_license = find_ruff_license(ruff_binary)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / (
        f"{deb['package-name']}_{project['version']}_{architecture}.deb"
    )

    with tempfile.TemporaryDirectory() as temporary_dir:
        package_root = Path(temporary_dir)/deb["package-name"]
        debian_dir = package_root/"DEBIAN"
        debian_dir.mkdir(parents=True)
        write_control_file(debian_dir, project, deb, architecture)
        copy_package(package_root, scripts)
        bundled_ruff = package_root/"usr/lib/hosker-utils/ruff"
        bundled_ruff.parent.mkdir(parents=True)
        shutil.copy2(ruff_binary, bundled_ruff)
        documentation_dir = package_root/"usr/share/doc/hosker-utils"
        shutil.copy2(ruff_license, documentation_dir/"ruff-copyright")
        normalize_permissions(package_root)
        bundled_ruff.chmod(0o755)
        subprocess.run(
            [
                "dpkg-deb",
                "--build",
                "--root-owner-group",
                str(package_root),
                str(output_path),
            ],
            check=True,
        )
    return output_path


def main() -> int:
    """Parse command-line arguments and build the package."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--ruff-binary", type=Path)
    arguments = parser.parse_args()
    output_path = build_deb(arguments.output_dir, arguments.ruff_binary)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
