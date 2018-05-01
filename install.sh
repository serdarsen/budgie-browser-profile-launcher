#!/bin/bash

PLUGIN_DIR="/usr/lib/budgie-desktop/plugins"

ICON_DIR="/usr/share/pixmaps"

declare -a icons=("browser-profile-launcher-1-symbolic.svg"
                "browser-profile-launcher-2-symbolic.svg"
                "browser-profile-launcher-3-symbolic.svg"
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
    echo "FAIL: Installation failed. Please note any errors above."
    exit 1
}

if [ ! -d "$ICON_DIR" ]
then
    echo "FAIL: The Icon directory does not exist: $ICON_DIR"
fi

function fail_icon() {
    echo "FAIL: Icon Installation failed. Please note any errors above."
}



# Actual installation
echo "Installing Budgie Browser Profile Launcher to $PLUGIN_DIR"

sudo rm -rf "${PLUGIN_DIR}/budgie-browser-profile-launcher" || fail
sudo cp -r ./src/budgie-browser-profile-launcher "${PLUGIN_DIR}/" || fail
sudo chmod -R 644 "${PLUGIN_DIR}/budgie-browser-profile-launcher/BudgieBrowserProfileLauncher.py" || fail

# icon installation
for icon in "${icons[@]}"
do
   sudo rm -rf "${ICON_DIR}/${icon}" || fail_icon
    sudo cp -r "./src/icons/${icon}" "${ICON_DIR}/" || fail_icon
    sudo chmod -R 644 "${ICON_DIR}/${icon}" || fail_icon
done

# restart the panel
budgie-panel --replace &

echo "Done. You should be able to add the applet to your panel now."