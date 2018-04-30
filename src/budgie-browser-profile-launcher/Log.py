#!/usr/bin/env python3

# This file is part of budgie-browser-profile-launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

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
            print(Log.ERROR_TAG + TAG + "; " + msg)

    #prints debug logs
    @staticmethod
    def d(TAG, msg):
        if (Log.logDebugOn):
            print(Log.DEBUG_TAG + TAG + "; " + msg)


    #prints info logs
    @staticmethod
    def i(TAG, msg):
        if (Log.logInfoOn):
            print(Log.INFO_TAG + TAG + "; " + msg)