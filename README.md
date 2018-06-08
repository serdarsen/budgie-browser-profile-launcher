Browser Profile Launcher
========

<br/>
Browser Profile Launcher is a Budgie Desktop applet for productivity. This applet lists and launches Chromium Browser and Google Chrome user profiles.<br/><br/>  


Evo Pop                    |  Arc Design
:-------------------------:|:-------------------------:
<img src="https://raw.githubusercontent.com/serdarsen/budgie-browser-profile-launcher/master/screenshots/screenshot2.gif" width="414"/>  |  <img src="https://raw.githubusercontent.com/serdarsen/budgie-browser-profile-launcher/master/screenshots/screenshot3.gif" width="414"/>

<br/>

Install
-------
```bash
   # !!! Before start, I'm not a professional linux developer. I wrote this applet and it works perfect on my ubuntu budgie (ubuntu 17:10 and 18.04, budgie version: 10.4,  device: acer aspire 5745g) . Please take your own risks and backups before install. Have fun!

   # Clone or download the repository
   git clone https://github.com/serdarsen/budgie-browser-profile-launcher.git

   # Go to the budgie-browser-profile-launcher directory (first)
   cd budgie-browser-profile-launcher

   # Configure the the installation
   mkdir build && cd build
   meson --buildtype plain --prefix=/usr --libdir=/usr/lib

   # Install
   sudo ninja install

   # To uninstall
   sudo ninja uninstall

   # You can add Browser Profile Launcher to your panel from Budgie Desktop Settings.

```

<br/>

Changelog
-------
### Added
* New temp window
* Add new person
* New incognito window
* Delete person
* add-new icon, butterfly icon,delete icon, incognito icon
* new stack pages
* new delete dialog
* new widgets and helpers
* fix all packages and classes
### Changed
* fix log
* fix sort
* Readme
### Removed
* launcher 3 icon

<br/>

References
-------

[budgie-desktop-examples](https://github.com/budgie-desktop/budgie-desktop-examples/tree/master/python_project)<br/>
[budgie-desktop applets](https://github.com/solus-project/budgie-desktop/tree/master/src/applets)<br/>
[budgie-menu](https://github.com/budgie-desktop/budgie-desktop/tree/master/src/applets/budgie-menu)<br/>
[user-indicator](https://github.com/solus-project/budgie-desktop/tree/master/src/applets/user-indicator)<br/>
[clock](https://github.com/solus-project/budgie-desktop/tree/master/src/applets/clock)

License
-------

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or at your option) any later version.

