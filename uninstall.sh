#!/bin/bash

PLUGIN_DIR="/usr/lib/budgie-desktop/plugins"

ICON_DIR="/usr/share/pixmaps"

declare -a icons=("browser-profile-launcher-1-symbolic.svg"
                "browser-profile-launcher-2-symbolic.svg"
                "browser-profile-launcher-butterfly-symbolic.svg"
                "browser-profile-launcher-add-new-symbolic.svg"
                "browser-profile-launcher-incognito-symbolic.svg"
                "browser-profile-launcher-delete-symbolic.svg"
                )

# Pre-install checks
if [ $(id -u) = 0 ]
then
    echo "FAIL: Please run this script as your normal user (not using sudo)."
    exit 1
fi

if [ ! -d "$PLUGIN_DIR" ]
then
    echo "FAIL: The Budgie plugin directory does not exist: $PLUGIN_DIR"
    exit 1
fi

function fail() {
    echo "FAIL: Uninstallation failed. Please note any errors above."
    exit 1
}


if [ ! -d "$ICON_DIR" ]
then
    echo "FAIL: The Icon directory does not exist: $ICON_DIR"
fi

function fail_icon() {
    echo "FAIL: Icon Uninstallation failed. Please note any errors above."
}


# Actual uninstallation
echo "Uninstalling Budgie Browser Profile Launcher to $PLUGIN_DIR"

sudo rm -rf "${PLUGIN_DIR}/budgie-browser-profile-launcher" || fail
sudo rm -rf "$HOME/.cache/budgie-browser-profile-launcher" || fail

# icon uninstallation
for icon in "${icons[@]}"
do
   sudo rm -rf "${ICON_DIR}/${icon}" || fail_icon
done

budgie-panel --replace &

echo "Done. Browser Profile Launcher Uninstalled."
