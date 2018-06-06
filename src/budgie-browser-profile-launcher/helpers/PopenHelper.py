#!/usr/bin/python3

# This file is part of Browser Profile Launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


from subprocess import Popen, PIPE, STDOUT
# DEVNULL hides Popen terminal outputs
try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')
from log.Log import Log
from log.Error import Error
from models.Browser import Browser


class PopenHelper():

    def __init__(self):

        self.TAG = "PopenHelper"
        self.log = Log("budgie-browser-profile-launcher")

        self.procs = []

    def popen(self, args):
        p = None
        try:
            p = Popen(args, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
            p.poll()
        # except IOError as err:
        #     self.log.e(self.TAG, "%s I/O error({0}): {1} : %s" % (args, err))
        # except ValueError as valueError:
        #     self.log.e(self.TAG, "%s ValueError : %s " % (args, valueError))
        # except TypeError as typeError:
        #     self.log.e(self.TAG, "%s TypeError : %s" % (args, typeError))
        except:
            # self.log.e(self.TAG, "%s Unexpected error: %s" % (args, sys.exc_info()[0]))
            self.log.e(self.TAG, Error.ERROR_7010 + " : %s" % args)

        return p

    def appendToProcs(self, proc):
        if proc is not None:
            self.procs.append(proc)

    def launchBrowserProfile(self, profile):
        if profile is not None:
            proc = self.popen([profile.getBrowser().getKey(), '--profile-directory=%s' % profile.getProfileKey()])
            self.appendToProcs(proc)

    def launchNewInconitoWindow(self, profile):
        if profile is not None:
            proc = self.popen([profile.getBrowser().getKey(), '--profile-directory=%s' % profile.getProfileKey(), '--incognito'])
            self.appendToProcs(proc)

    def launchNewTempWindow(self, browser):
        if(browser is not None and browser.getKey() is Browser.KEY_CHROMIUM):
            self.popen([browser.getKey(), '--temp-profile'])

    def addNewProfile(self, browser, name):
        if browser is not None and name is not None:
            proc = self.popen([browser.getKey(), '--profile-directory=%s' % name])
            self.appendToProcs(proc)

    def killBrowser(self, browser):
        # self.log.d(self.TAG, "killBrowser browser : " + browser.getName())
        self.terminateProcs()
        if browser is not None:
            # self.log.d(self.TAG, "killBrowser pKill : " + browser.getName())
            self.popen(['pkill', browser.getShort()])

    def deleteDir(self, path):
        # self.log.d(self.TAG, "deleteDir path : " + path)
        if path is not None:
            # self.log.d(self.TAG, "deleteDir path is not None path : " + path)
            self.popen(['rm', '-rf', path])

    def terminateProcs(self):
        # self.log.d(self.TAG, "killProcs")
        # self.log.d(self.TAG, "killProcs len(self.procs) : %s" % len(self.procs))
        for proc in self.procs:
            # self.log.d(self.TAG, "proc.terminate")
            proc.terminate()
        self.procs = []
