#!/bin/bash

PLUGIN_DIR="/usr/lib/budgie-desktop/plugins"

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

# Actual installation
echo "Uninstalling Budgie Browser Profile Launcher to $PLUGIN_DIR"

sudo rm -rf "${PLUGIN_DIR}/budgie-browser-profile-launcher" || fail
budgie-panel --replace &

echo "Done. Browser Profile Launcher Uninstalled."
