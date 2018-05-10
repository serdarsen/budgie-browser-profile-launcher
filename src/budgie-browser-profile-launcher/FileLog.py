#!/usr/bin/env python3

# This file is part of Browser Profile Launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import os, errno
import datetime

class FileLog():

    TAG = "FileLog"
    logErrorOn = True
    logDebugOn = False
    logInfoOn = False

    ERROR_TAG = "Log e: "
    DEBUG_TAG = "Log d: "
    INFO_TAG = "Log i: "

    userHomePath = ""
    appCacheFolderName = ""
    appCacheFilePath = ""
    appLogFilePath = ""

    def __init__(self, appConfigFolderName):

        self.appCacheFolderName = appConfigFolderName

        try:
            self.userHomePath = os.path.expanduser("~")
            self.appCacheFilePath = self.userHomePath + "/.cache/" + self.appCacheFolderName
            self.makeDirIfNotExist(self.appCacheFilePath)
            self.appLogFilePath = self.appCacheFilePath + "/log"
        except:
            Log.e(self.TAG, "error while loading log file")

    # gets datatime
    def getDateTime(self):
        return datetime.datetime.now()

    #makes dir
    def makeDirIfNotExist(self, path):
        if (path is not ""):
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    # writes error logs into the log file
    def e(self, TAG, msg):
        if (self.logErrorOn):
            try:
                with open(self.appLogFilePath, "a+") as file:
                    file.write("[%s] %s %s ; %s\n" % (self.getDateTime(), self.ERROR_TAG, TAG, str(msg)))
            except:
                Log.e(self.TAG, "error while saving error log")

    # writes debug logs into the log file
    def d(self, TAG, msg):
        if (self.logDebugOn):
            try:
                with open(self.appLogFilePath, "a+") as file:
                    file.write("[%s] %s %s ; %s\n" % (self.getDateTime(), self.DEBUG_TAG, TAG, str(msg)))
            except:
                Log.e(self.TAG, "error while saving debug log")

    # writes info logs into the log file
    def i(self, TAG, msg):
        if (self.logInfoOn):
            try:
                with open(self.appLogFilePath, "a+") as file:
                    file.write("[%s] %s %s ; %s\n" % (self.getDateTime(), self.INFO_TAG, TAG, str(msg)))
            except:
                Log.e(self.TAG, "error while saving info log")


    #just reminder
    # def tryExceptTemplate(self):
    #     try:
    #         #the job here
    #     except IOError as err:
    #         self.fileLog.e(self.TAG, "I/O error({0}): {1} : %s" % err)
    #     except ValueError:
    #         self.fileLog.e(self.TAG, "Could not convert data to an integer.")
    #     except:
    #         self.fileLog.e(self.TAG, "Unexpected error: %s" % sys.exc_info()[0])
    #         raise

class Log():

    logErrorOn = True
    logDebugOn = False
    logInfoOn = True

    ERROR_TAG = "Log e: "
    DEBUG_TAG = "Log d: "
    INFO_TAG = "Log i: "

    #prints error logs
    @staticmethod
    def e(TAG, msg):
        if (Log.logErrorOn):
            print("[%s] %s %s ; %s" % (datetime.datetime.now(), Log.INFO_TAG, TAG, str(msg)))

    #prints debug logs
    @staticmethod
    def d(TAG, msg):
        if (Log.logDebugOn):
            print("[%s] %s %s ; %s" % (datetime.datetime.now(), Log.DEBUG_TAG, TAG, str(msg)))


    #prints info logs
    @staticmethod
    def i(TAG, msg):
        if (Log.logInfoOn):
            print("[%s] %s %s ; %s" % (datetime.datetime.now(), Log.INFO_TAG, TAG, str(msg)))
