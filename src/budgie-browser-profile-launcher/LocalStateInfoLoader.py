#!/usr/bin/env python3

# This file is part of budgie-browser-profile-launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from os.path import expanduser
import json
import sys
from FileLog import FileLog
import os.path

class LocalStateInfoLoader():

    TAG = "LocalStateInfoLoader"
    home_dir = ""
    chromiumPath = ""
    chromePath = ""
    chromium_data = None
    chrome_data = None

    def __init__(self):

        try:
            self.home_dir = expanduser("~")
            self.chromiumPath = self.home_dir + "/.config/chromium/Local State"
            self.chromePath = self.home_dir + "/.config/google-chrome/Local State"
        except:
           self.fileLog.e(self.TAG, "error_1015 get home_dir error")

        self.profilesList = []
        self.fileLog = FileLog("budgie-browser-profile-launcher")

    def getProfiles(self):
        self.profilesList = []
        profilesListChromium = []

        if(os.path.exists(self.chromiumPath)):
            try:
                with open(self.chromiumPath, "r") as file:
                    self.chromium_data = json.load(file)
            except:
                self.fileLog.e(self.TAG, "error_5110")

        if(self.chromium_data is not None):
            try:
                profiles_data = self.chromium_data['profile']
                info_cache_data = profiles_data['info_cache']
                for profile_key in info_cache_data:
                    profile_data = info_cache_data[profile_key]
                    profile_name = profile_data['name']
                    profilesListChromium.append(Profile(True, False, profile_key, profile_name))
                profilesListChromium = sorted(profilesListChromium, key=lambda x: x.getProfileName().upper(), reverse=False)

            except :
                self.fileLog.e(self.TAG, "error_5111")

        profilesListChrome = []

        if (os.path.exists(self.chromePath)):
            try:
                with open(self.chromePath, "r") as file:
                    self.chromium_data = json.load(file)
            except:
                self.fileLog.e(self.TAG, "error_5112")

        if(self.chrome_data is not None):
            try:
                profiles_data = self.chrome_data['profile']
                info_cache_data = profiles_data['info_cache']
                for profile_key in info_cache_data:
                    profile_data = info_cache_data[profile_key]
                    profile_name = profile_data['name']
                    profilesListChrome.append(Profile(False, True, profile_key, profile_name))
                profilesListChrome = sorted(profilesListChrome, key=lambda x: x.getProfileName().upper(), reverse=False)
            except:
                self.fileLog.e(self.TAG, "error_5113")

        self.profilesList = profilesListChromium + profilesListChrome

        return self.profilesList


class Profile():

    isChromium  = False
    isChrome = False

    def __init__(self, isChromium, isChrome, profileKey, profileName):
        self.isChromium = isChromium
        self.isChrome = isChrome
        self.profileKey = profileKey
        self.profileName = profileName

    def getProfileKey(self):
        return self.profileKey

    def getProfileName(self):
        return self.profileName

    def isChromiumBrowser(self):
        return self.isChromium

    def isGoogleChrome(self):
        return self.isChrome
