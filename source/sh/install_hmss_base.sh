#!/bin/sh

### This script install His Majesty's Software Suite.

set -e  # Crash on the first non-zero exit code.

# Local constants.
NO_COLOUR="\033[0m"
RED="\033[0;31m"
LIGHT_PURPLE="\033[0;35m"
CYAN="\033[0;36m"
COLOUR=$LIGHT_PURPLE

# To be replaced.
ESSENTIAL_APT_PACKAGES="%ESSENTIAL_APT_PACKAGES%"
INSTALL_CHROME=%INSTALL_CHROME%
NON_ESSENTIAL_APT_PACKAGES="%NON_ESSENTIAL_APT_PACKAGES%"
ROYAL_REPOS="%ROYAL_REPOS%"
CLONE_METHOD="%CLONE_METHOD%"
GIT_HOST="%GIT_HOST%"
GIT_ACCOUNT_NAME="%GIT_ACCOUNT_NAME%"
PATH_TO_WP="%PATH_TO_WALLPAPER%"  # WP = wallpaper

##############
# ESSENTIALS #
##############

# Do this in the home directory.
cd

# Get sudo.
echo "${COLOUR}I'm going to need superuser privileges to install HMSS..."
sudo echo "Superuser privileges: activate!"

# Ensure APT is up to date.
sudo apt update
sudo apt upgrade --yes

# Install essential APT packages.
if [ ! $ESSENTIAL_APT_PACKAGES ]; then
    echo "${COLOUR}No essential APT packages to install."
else
    sudo apt install --yes $ESSENTIAL_APT_PACKAGES
fi

##################
# NON-ESSENTIALS #
##################

# Install non-essential APT packages.
if [ ! $NON_ESSENTIAL_APT_PACKAGES ]; then
    echo "${COLOUR}No non-essential APT packages to install."
else
    sudo apt install --yes $NON_ESSENTIAL_APT_PACKAGES
fi

# Make our Git URL stem.
if [ $CLONE_METHOD = "https" ]; then
    git_url_stem="https://$GIT_HOST/$GIT_ACCOUNT_NAME"
elif [ $CLONE_METHOD = "ssh" ]; then
    git_url_stem="git@$GIT_HOST:$GIT_ACCOUNT_NAME"
else
    echo "Bad CLONE_METHOD: $CLONE_METHOD"
    exit 1
fi

# Clone royal repos.
for repo_name in $ROYAL_REPOS; do
    if [ -d $repo_name ]; then
        echo "${COLOUR}Looks like we've already got $repo_name..."
    else
        git clone $git_url_stem/$repo_name
    fi
done

# Change wallpaper.
gsettings set org.gnome.desktop.background picture-uri file:///$PATH_TO_WP

###########
# WRAP UP #
###########

# All good.
echo "${COLOUR}All good. :)"
