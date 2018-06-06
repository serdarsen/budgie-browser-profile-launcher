#!/usr/bin/python3

# This file is part of Browser Profile Launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


import re


class SortHelper():

    def convert(self, text):
        if text.isdigit():
            return int(text)
        else:
            return text.lower()

    def naturalSortMyProfiles(self, profile):
        key = profile.getProfileName()
        cList = []
        for c in re.split('([0-9]+)', key):
            cList.append(self.convert(c))
        return cList

    def sortedProfiles(self, listToSort):
        return sorted(listToSort, key=self.naturalSortMyProfiles)