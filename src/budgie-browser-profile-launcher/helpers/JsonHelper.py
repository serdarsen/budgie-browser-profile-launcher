#!/usr/bin/python3

# This file is part of Browser Profile Launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


import json
from log.Log import Log
from log.Error import Error
import os.path

class JsonHelper():


    def __init__(self):
        self.TAG = "JsonHelper"
        self.log = Log("budgie-browser-profile-launcher")


    def setDictIfNone(self, data, key):
        if data is not None and key is not None:
            if data.get(key, None) is None:
                data[key] = {}
            return data[key] 

    def setListIfNone(self, data, key):
        if data is not None and key is not None:
            if data.get(key, None) is None:
                data[key] = []    
            return data[key]
                
    def readData(self, filePath):
        if os.path.exists(filePath):
            try:
                with open(filePath) as json_file:
                    data = json.load(json_file)
                    return data
            except IOError as err:
                self.log.e(self.TAG, Error.ERROR_1010)

    def writeData(self, filePath, data):
        if os.path.exists(filePath):
            try:
                with open(filePath, 'w') as outfile:
                    json.dump(data, outfile, indent=4)
            except:
                self.log.e(self.TAG, Error.ERROR_1011)