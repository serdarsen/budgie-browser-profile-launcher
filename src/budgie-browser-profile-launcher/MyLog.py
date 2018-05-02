#!/usr/bin/env python3

# This file is part of U Brightness Controller

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import os
import errno
import datetime

class MyLog():

    TAG = "MyLog"
    logErrorOn = True
    logDebugOn = False
    logInfoOn = True

    ERROR_TAG = "MyLog e: "
    DEBUG_TAG = "MyLog d: "
    INFO_TAG = "MyLog i: "

    userHomePath = os.path.expanduser("~")
    appCacheFolderName = "u-brightness-controller"
    appCacheFolderPath = userHomePath + "/.cache/" + appCacheFolderName
    appLogFilePath = appCacheFolderPath + "/log"

    # gets datatime
    @staticmethod
    def getDateTime():
        return datetime.datetime.now()

    # makes dir
    @staticmethod
    def makeDirIfNotExist(path):
        if (path is not ""):
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    # writes error logs into the log file
    @staticmethod
    def e(TAG, msg):
        if (MyLog.logErrorOn):
            print ("[%s] %s %s : %s" % (datetime.datetime.now(), MyLog.ERROR_TAG, TAG, str(msg)))
            try:
                MyLog.makeDirIfNotExist(MyLog.appCacheFolderPath)
                with open(MyLog.appLogFilePath, "a+") as logFile:
                    logFile.write("[%s] %s %s : %s\n" % (MyLog.getDateTime(), MyLog.ERROR_TAG, TAG, str(msg)))
            except:
                print(MyLog.TAG, " error while saving error log")

    # writes debug logs into the log file
    @staticmethod
    def d(TAG, msg):
        if (MyLog.logDebugOn):
            print ("[%s] %s %s : %s" % (datetime.datetime.now(), MyLog.DEBUG_TAG, TAG, str(msg)))
            try:
                MyLog.makeDirIfNotExist(MyLog.appCacheFolderPath)
                with open(MyLog.appLogFilePath, "a+") as logFile:
                    logFile.write("[%s] %s %s : %s\n" % (MyLog.getDateTime(), MyLog.DEBUG_TAG, TAG, str(msg)))
            except:
                print(MyLog.TAG + " error while saving debug log")


    # writes info logs into the log file
    @staticmethod
    def i(TAG, msg):
        print ("[%s] %s %s : %s" % (datetime.datetime.now(), MyLog.INFO_TAG, TAG, str(msg)))
        if (MyLog.logInfoOn):
            try:
                MyLog.makeDirIfNotExist(MyLog.appCacheFolderPath)
                with open(MyLog.appLogFilePath, "a+") as logFile:
                    logFile.write("[%s] %s %s : %s\n" % (MyLog.getDateTime(), MyLog.INFO_TAG, TAG, str(msg)))
            except:
                print(MyLog.TAG, " error while saving info log")


    # just reminder
    # def tryExceptTemplate(self):
    #     try:
    #         #the job here
    #     except IOError as err:
    #         print(MyLog.TAG, "I/O error({0}): {1} : %s" % err)
    #     except ValueError:
    #         print(MyLog.TAG, "Could not convert data to an integer.")
    #     except:
    #         print(MyLog.TAG, "Unexpected error: %s" % sys.exc_info()[0])
    #         raise