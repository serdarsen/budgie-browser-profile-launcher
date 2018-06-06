#!/usr/bin/python3

# This file is part of Browser Profile Launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


class Profile():

    def __init__(self, browser, profileKey, profileName):
        self.browser = browser
        self.profileKey = profileKey
        self.profileName = profileName

    def getProfileKey(self):
        return self.profileKey

    def getProfileName(self):
        return self.profileName

    def isChromiumBrowser(self):
        if self.browser is not None:
            return self.browser.isChromiumBrowser()
        else:
            return False

    def isGoogleChrome(self):
        if self.browser is not None:
            return self.browser.isGoogleChrome()
        else:
            return False

    def getBrowser(self):
        return self.browser