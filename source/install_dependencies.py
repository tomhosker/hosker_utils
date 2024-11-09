"""
This code defines a function which installs a given list of PIP packages.
"""

# Standard imports.
import subprocess

#############
# FUNCTIONS #
#############

def install_dependency(package: str) -> bool:
    """
    Install a PIP package from a given package string, e.g. "pytest",
    "pylint>=2.12.2", etc.
    """
    try:
        subprocess.run(["pip", "install", package], check=True)
    except subprocess.CalledProcessError:
        return False
    return True

def install_dependencies(packages: list[str]) -> bool:
    """ As above, but for several packages. """
    for package in packages:
        local_result = \
            install_dependency(package)
        if not local_result:
            return False
    return True

def install_apt_package(
    package: str,
    yes: bool = True,
    raise_error: bool = True,
    quiet: bool = False
) -> bool:
    """ Obviously, this will only work in a Debian-based system. """
    args = ["sudo", "apt-get", "install"]
    if yes:
        args += ["--yes"]
    args += [package]
    if not quiet:
        print(f"I'm going to need superuser privileges to install {package}")
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        if raise_error:
            raise
        return False
    return True

def install_apt_packages(
    packages: list[str],
    quiet: bool = False,
    **kwargs
) -> bool:
    """ An iterative version of the above. """
    if not quiet:
        print(
            "I'm going to need superuser privileges to install %s"
            % ", ".join(packages)
        )
    for package in packages:
        if not install_apt_package(package, quiet=False, **kwargs):
            return False
    return True
