#!/usr/bin/python3

# This file is part of Browser Profile Launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


from os.path import expanduser
import os.path
from models.Profile import Profile
from models.Browser import Browser
from log.Log import Log
from log.Error import Error
from helpers.JsonHelper import JsonHelper
import time


class LocalStateHelper():

    def __init__(self):

        self.TAG = "LocalStateHelper"
        self.log = Log("budgie-browser-profile-launcher")
        self.jsonHelper = JsonHelper()

        self.localStateFileName = "Local State"
        self.lastProfileNum = 0
        self.lastPersonNum = 0

        self.home_dir = expanduser("~")
        self.chromiumConfigPath = self.home_dir + "/.config/chromium/"
        self.chromeConfigPath = self.home_dir + "/.config/google-chrome/"
        self.chromiumCachePath = self.home_dir + "/.cache/chromium/"
        self.chromeCachePath = self.home_dir + "/.cache/google-chrome/"

        self.availbleBrowsers = []

    def isChromiumAvailable(self):
        return os.path.exists(self.chromiumConfigPath)

    def isChromeAvailable(self):
        return os.path.exists(self.chromeConfigPath)

    def getNewProfileKey(self, browser):
        profiles = None

        try:

            if browser is not None:
                if browser.getKey() is Browser.KEY_CHROMIUM:
                    profiles = self.getChromiumProfiles()
                elif browser.getKey() is Browser.KEY_CHROME:
                    profiles = self.getChromeProfiles()

            nums = []

            if profiles is not None:
                for profile in profiles:
                    key = profile.getProfileKey()
                    # self.log.d(self.TAG, "key : %s" % key)
                    if "Profile" in key:
                        keySplit = key.split(" ")
                        # self.log.d(self.TAG, "len(keySplit) : %s" % len(keySplit))
                        if len(keySplit) > 1:
                            num = int(keySplit[1])
                            nums.append(num)
            if not nums:
                newKey = "Profile 1"
            else:
                if self.lastProfileNum is not 0:
                    self.lastProfileNum = self.lastProfileNum + 1
                    newKey = "Profile %s" % self.lastProfileNum
                else:
                    self.lastProfileNum = max(nums) + 1
                    newKey = "Profile %s" % self.lastProfileNum

        except:
            newKey = "Profile %s" % int(round(time.time() * 1000))

        return newKey

    def getProfilesFromData(self, path, browser):
        data = self.jsonHelper.readData(path)
        profiles = []
        if data is not None:
            try:
                rootProfileData = data['profile']
                infoCacheData = rootProfileData['info_cache']
                for profileKey in infoCacheData:
                    profileData = infoCacheData[profileKey]
                    profileName = profileData['name']
                    profiles.append(Profile(browser, profileKey, profileName))
            except:
                self.log.e(self.TAG, Error.ERROR_6012)
        return profiles


    def deleteProfileFromData(self, path, profile):
        profileToRemovePath = path + profile.getProfileKey()
        filePath = path + self.localStateFileName
        profileKeyToRemove = profile.getProfileKey()
        data = self.jsonHelper.readData(filePath)
        profiles = []
        if data is not None:
            self.removeProfileFromRootProfile(data, profileKeyToRemove)
            #self.addProfileToProfilesDeleted(data, profileToRemovePath)
            self.removeProfileFromLastActiveProfiles(data, profileKeyToRemove)
            self.removeProfileFromLastUsed(data, profileKeyToRemove)
            self.jsonHelper.writeData(filePath, data)

    def removeProfileFromRootProfile(self, data, profileKeyToRemove):
        try:
            rootProfileData = data['profile']
            infoCacheData = rootProfileData['info_cache']
            for profileKey in infoCacheData:
                profileData = infoCacheData[profileKey]
                profileName = profileData['name']
                if profileKey == profileKeyToRemove:
                    infoCacheData.pop(profileKey)
                    break
        except:
            self.log.e(self.TAG, Error.ERROR_6013)

    def removeProfileFromLastActiveProfiles(self, data, profileKeyToRemove):
        rootProfileData = data.get("profile", None)
        lastActiveProfiles = rootProfileData.get("last_active_profiles", None)
        if lastActiveProfiles is not None:
            if profileKeyToRemove in lastActiveProfiles:
                lastActiveProfiles.remove(profileKeyToRemove)

    def removeProfileFromLastUsed(self, data, profileKeyToRemove):
        rootProfileData = data.get("profile", None)
        lastUsed = rootProfileData.get("last_used", None)
        if lastUsed is not None:
            if lastUsed == profileKeyToRemove:
                rootProfileData["last_used"] = ""

    def addProfileToProfilesDeleted(self, data, profileToRemovePath):
        dataProfiles = self.jsonHelper.setDictIfNone(data, "profiles")
        profilesDeleted = self.jsonHelper.setListIfNone(dataProfiles, "profiles_deleted")
        profilesDeleted.append(profileToRemovePath)

    def getChromiumProfiles(self):
        return self.getProfilesFromData(self.chromiumConfigPath + self.localStateFileName, Browser(Browser.CHROMIUM))

    def getChromeProfiles(self):
        return self.getProfilesFromData(self.chromeConfigPath + self.localStateFileName, Browser(Browser.CHROME))

    def getProfiles(self):
        profiles = []
        chromiumProfiles = self.getChromiumProfiles()
        chromeProfiles = self.getChromeProfiles()
        profiles = chromiumProfiles + chromeProfiles

        return profiles

    def delete(self, profile):
        # self.log.d(self.TAG, "delete")
        if profile.isChromiumBrowser():
            self.deleteProfileFromData(self.chromiumConfigPath, profile)
        elif profile.isGoogleChrome():
            self.deleteProfileFromData(self.chromeConfigPath, profile)

    def getProfileConfigPath(self, profile):
        if profile.isChromiumBrowser():
            return self.chromiumConfigPath + profile.getProfileKey()
        elif profile.isGoogleChrome():
            return self.chromeConfigPath + profile.getProfileKey()

    def getProfileCachePath(self, profile):
        if profile.isChromiumBrowser():
            return self.chromiumCachePath + profile.getProfileKey()
        elif profile.isGoogleChrome():
            return self.chromeCachePath + profile.getProfileKey()