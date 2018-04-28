#!/usr/bin/env python3

# This file is part of budgie-browser-profile-launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from os.path import expanduser
import json
from Log import Log

class LocalStateInfoLoader():

    TAG = "LocalStateInfoLoader"

    def __init__(self):

        try:
            self.home_dir = expanduser("~")
        except:
            Log.e("error_1015 get home_dir error")

        self.chromium_data = None
        self.chrome_data = None
        self.profilesList = []

    def getProfiles(self):
        self.profilesList = []
        profilesListChromium = []
        try:
            self.chromium_data = json.load(open(self.home_dir + '/.config/chromium/Local State'))
        except:
            Log.e(self.TAG, "error_1016 chromium-browser Local State file load error")

        if(self.chromium_data is not None):
            try:
                profiles_data = self.chromium_data['profile']
                info_cache_data = profiles_data['info_cache']
                for profile_key in info_cache_data:
                    profile_data = info_cache_data[profile_key]
                    profile_name = profile_data['name']
                    profilesListChromium.append(Profile(True, False, profile_key, profile_name))
                profilesListChromium = sorted(profilesListChromium, key=lambda x: x.getProfileName().upper(), reverse=False)
            except:
                Log.e(self.TAG, "error_1012 getProfiles error")

        profilesListChrome = []
        try:
            self.chrome_data = json.load(open(self.home_dir + '/.config/google-chrome/Local State'))
        except:
            Log.e(self.TAG, "error_1013 google-chrome Local State file load error")

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
                Log.e(self.TAG, "error_1014 getProfiles error")

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
