#!/usr/bin/python3

# This file is part of Browser Profile Launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


class Browser():

    CHROMIUM = "1"
    CHROME = "2"
    isChromium = False
    isChrome = False

    NAME_CHROMIUM = "Chromium"
    SHORT_CHROMIUM = "chromium"
    KEY_CHROMIUM = "chromium-browser"

    NAME_CHROME = "Google chrome"
    SHORT_CHROME = "chrome"
    KEY_CHROME = "google-chrome"

    def __init__(self, type):

        if(type is self.CHROMIUM):

            self.name = self.NAME_CHROMIUM
            self.short = self.SHORT_CHROMIUM
            self.key = self.KEY_CHROMIUM
            self.isChromium = True

        elif(type is self.CHROME):

            self.name = self.NAME_CHROME
            self.short = self.SHORT_CHROME
            self.key = self.KEY_CHROME
            self.isChrome = True


    def getKey(self):
        return self.key

    def getName(self):
        return self.name

    def getShort(self):
        return self.short


    def isChromiumBrowser(self):
        return self.isChromium

    def isGoogleChrome(self):
        return self.isChrome