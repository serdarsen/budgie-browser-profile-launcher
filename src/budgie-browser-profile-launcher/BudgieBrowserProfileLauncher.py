#!/usr/bin/env python3

# This file is part of budgie-browser-profile-launcher

# Copyright © 2015-2017 Ikey Doherty <ikey@solus-project.com>
# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import gi.repository
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, GObject, Gtk, Gdk
import os.path
from subprocess import Popen, PIPE, STDOUT

#DEVNULL hides Popen terminal outputs
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

from LocalStateInfoLoader import LocalStateInfoLoader
from FileLog import FileLog

class BudgieBrowserProfileLauncher(GObject.GObject, Budgie.Plugin):
    #This is simply an entry point into your Budgie Applet implementation. Note you must always override Object, and implement Plugin.

    # Good manners, make sure we have unique name in GObject type system
    __gtype_name__ = "io_serdarsen_github_budgie_browser_profile_launcher"

    def __init__(self):

        #Initialisation is important.
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        #This is where the real fun happens. Return a new Budgie.Applet instance with the given UUID. The UUID is determined by the BudgiePanelManager, and is used for lifetime tracking.
        return BudgieBrowserProfileLauncherApplet(uuid)

class BudgieBrowserProfileLauncherApplet(Budgie.Applet):
    #Budgie.Applet is in fact a Gtk.Bin

    APPINDICATOR_ID = "io_serdarsen_github_budgie_browser_profile_launcher"
    TAG = "BrowserProfileLauncherApplet"
    manager = None
    menuListBoxMarginTop = 0
    menuListBoxMarginBottom = 0
    menuListBoxMarginLeft = 0
    menuListBoxMarginRight = 0
    menuButtonContentMarginTop = 0 #3
    menuButtonContentMarginBottom = 0 #3
    menuScrollViewMarginTop = 0
    menuScrollViewMarginBottom = 3
    popover = None
    popoverMaxHeight = 480
    popoverBaseHeight = menuListBoxMarginTop + menuListBoxMarginBottom + menuScrollViewMarginTop + menuScrollViewMarginBottom
    popoverHeight = popoverBaseHeight
    popoverHeightOffset = 10
    popoverWidth = 270
    menuListRowHeight = 38
    menuListBoxSpacing = 6
    dir_path = None
    iconChromiumPath = None
    iconChromePath = None
    iconIndicatorPath = None
    profiles = []

    def __init__(self, uuid):

        Budgie.Applet.__init__(self)

        self.fileLog = FileLog("budgie-browser-profile-launcher")


        self.fileLog.i(self.TAG, "BudgieBrowserProfileLauncherApplet initialising ...")

        self.localStateInfoLoader = LocalStateInfoLoader()

        #file dirs
        try:
            self.dir_path = os.path.dirname(os.path.realpath(__file__))
            self.iconChromiumPath = self.dir_path + "/icon_chromium.svg"
            self.iconChromePath = self.dir_path + "/icon_chrome.svg"
            self.iconIndicatorPath = self.dir_path + "/icon_indicator.svg"
        except:
            self.fileLog.e(self.TAG, "error_3010")

        #indicator icon and box
        self.indicatorBox = Gtk.EventBox()
        if(self.iconIndicatorPath is not None):
            self.iconIndicator = Gtk.Image()
            self.iconIndicator.set_from_file(self.iconIndicatorPath)
            self.indicatorBox.add(self.iconIndicator)

        self.indicatorBox.show_all()

        self.add(self.indicatorBox)
        self.popover = Budgie.Popover.new(self.indicatorBox)
        self.popover.set_default_size(self.popoverWidth, self.popoverHeight)

        #holds all popover content
        self.mainlayout = Gtk.Box(Gtk.Orientation.VERTICAL, 0)

        # Holds all the rows
        self.menuListBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.menuListBoxSpacing);
        self.menuListBox.props.valign = Gtk.Align.END

        # Must call after popover, localStateInfoLoader,
        # menuListBox, iconChromePath and iconChromiumPath inits
        self.updateProfileList()

        self.mainScrollView = Gtk.ScrolledWindow(None, None)
        self.mainScrollView.set_overlay_scrolling(True)
        self.mainScrollView.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        # Hides dotted lines when scroll
        self.mainScrollView.get_style_context().add_class("budgie-menu")

        self.menuListBox.set_margin_top(self.menuListBoxMarginTop)
        self.menuListBox.set_margin_bottom(self.menuListBoxMarginBottom)
        self.menuListBox.set_margin_left(self.menuListBoxMarginLeft)
        self.menuListBox.set_margin_right(self.menuListBoxMarginRight)

        self.mainScrollView.set_margin_top(self.menuScrollViewMarginTop)
        self.mainScrollView.set_margin_bottom(self.menuScrollViewMarginBottom)


        self.mainScrollView.add(self.menuListBox)
        self.mainlayout.pack_start(self.mainScrollView, True, True, 0)

        self.popover.add(self.mainlayout)

        self.popover.get_child().show_all()
        self.indicatorBox.show_all()
        self.show_all()
        self.indicatorBox.connect("button-press-event", self.on_press)

    def on_press(self, box, e):
        self.fileLog.i(self.TAG, "on_press")
        if e.button != 1:
            return Gdk.EVENT_PROPAGATE
        if self.popover.get_visible():
            self.popover.hide()
        else:
            self.updateProfileList()
            self.manager.show_popover(self.indicatorBox)
        return Gdk.EVENT_STOP

    #hides popover if it is visible
    def hidePopover(self):
        if(self.popover is not None):
            if self.popover.get_visible():
                self.popover.hide()

    #listens menu button clicks
    def listMenuButtonClicked(self, button):
        self.hidePopover()
        try:
            profile = button.getProfile()
            self.launchBrowserProfile(profile)
        except:
            self.fileLog.e(self.TAG, "error_1011")

    #this is an original method from budgie applet python example on github
    def do_update_popovers(self, manager):
        self.manager = manager
        self.manager.register_popover(self.indicatorBox, self.popover)

    #Launches browser profile
    def launchBrowserProfile(self, profile):

        if (profile.isChromiumBrowser()):
            try:
                p1 = Popen(['chromium-browser', '--profile-directory=%s' % profile.getProfileKey()], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
                p1.poll()
            except:
                self.fileLog.e(self.TAG, "error_1010")

        elif (profile.isGoogleChrome()):
            try:
                p2 = Popen(['google-chrome', '--profile-directory=%s' % profile.getProfileKey()], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
                p2.poll()
            except:
                self.fileLog.e(self.TAG, "error_1010")

    #updates profiles in popover
    def updateProfileList(self):

        #cleans the list
        if(self.menuListBox.get_children() is not None):
            for child in self.menuListBox.get_children():
                self.menuListBox.remove(child)

        try:
            self.profiles = self.localStateInfoLoader.getProfiles()
        except :
            self.fileLog.e(self.TAG, "error_1015")

        self.popoverHeight = self.popoverBaseHeight

        for profile in self.profiles:

            menuButton = MenuButton(profile)
            menuButton.set_size_request(self.popoverWidth - 2, self.menuListRowHeight)
            ##menuButton.set_tooltip_text(profile.getProfileKey())

            # Makes buttons default color same as its parent
            menuButton.get_style_context().add_class("flat")
            menuButtonContent = Gtk.Box(Gtk.Orientation.HORIZONTAL, 0)

            #menuLabel
            menuLabel = Gtk.Label(profile.getProfileName(), xalign=0)
            menuLabel.set_margin_left(4)

            #adds list menuIcon to menuIconBox
            if(profile.isChromiumBrowser()):
                if(self.iconChromiumPath is not None):
                    iconChromium = Gtk.Image()
                    iconChromium.set_from_file(self.iconChromiumPath)
                    menuButtonContent.pack_start(iconChromium, False, False, 0)

            elif(not profile.isChromiumBrowser()):
                if(self.iconChromePath is not None):
                    iconChrome = Gtk.Image()
                    iconChrome.set_from_file(self.iconChromePath)
                    menuButtonContent.pack_start(iconChrome, False, False, 0)

            #adds label to menuButtonContent
            menuButtonContent.pack_start(menuLabel, True, True, 0)
            menuButtonContent.set_margin_top(self.menuButtonContentMarginTop)
            menuButtonContent.set_margin_bottom(self.menuButtonContentMarginBottom)

            menuButton.connect("clicked", self.listMenuButtonClicked)
            menuButton.add(menuButtonContent)

            self.menuListBox.add(menuButton)

        profilesLenght = len(self.profiles)
        self.popoverHeight = (self.menuListRowHeight * (profilesLenght + 1)) + (self.menuListBoxSpacing * profilesLenght) + self.popoverBaseHeight
        if(self.popoverHeight > self.popoverMaxHeight):
            self.popoverHeight = self.popoverMaxHeight
        self.popover.get_child().show_all()
        self.popover.resize(self.popoverWidth, self.popoverHeight)

class MenuButton(Gtk.Button):
    def __init__(self, profile):
        super(Gtk.Button, self).__init__()
        self.profile = profile

    def getProfile(self):
        return self.profile
