#!/usr/bin/python3

# This file is part of Browser Profile Launcher

# Copyright © 2015-2017 Ikey Doherty <ikey@solus-project.com>
# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
import os.path
from helpers.LocalStateHelper import LocalStateHelper
from helpers.SortHelper import SortHelper
from helpers.PopenHelper import PopenHelper
from widgets.DirectionalButton import DirectionalButton
from widgets.Dialog import Dialog
from widgets.ListView import ListView
from widgets.LauncherButton import LauncherButton
from widgets.BrowserButton import BrowserButton
from widgets.ProfileButton import ProfileButton
from models.Browser import Browser
from log.Log import Log


class BrowserProfileLauncher(GObject.GObject, Budgie.Plugin):
    ## This is simply an entry point into your Budgie Applet implementation. Note you must always override Object, and implement Plugin.

    ## Good manners, make sure we have unique name in GObject type system
    __gtype_name__ = "io_serdarsen_github_budgie_browser_profile_launcher"

    def __init__(self):
        ## Initialisation is important.
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        ## This is where the real fun happens. Return a new Budgie.Applet instance with the given UUID. The UUID is determined by the BudgiePanelManager, and is used for lifetime tracking.
        return BrowserProfileLauncherApplet(uuid)


class BrowserProfileLauncherApplet(Budgie.Applet):
    ## Budgie.Applet is in fact a Gtk.Bin

    def __init__(self, uuid):

        self.TAG = "BrowserProfileLauncher"
        self.APPINDICATOR_ID = "io_serdarsen_github_budgie_browser_profile_launcher"
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.manager = None
        self.popover = None
        self.popoverHeightOffset = 20
        self.popoverMinHeight = 150
        self.popoverMaxHeight = 480
        self.popoverMinWidth = 256
        self.popoverHeight = 0
        self.popoverWidth = 230
        self.launcherButtonHeight = 36
        self.lenProfiles = 0
        self.launcherButtons = []
        self.availableBrowsers = []
        self.currentProfile = None
        self.currentBrowser = None
        self.chromiumBrowser = None
        self.chromeBrowser = None

        Budgie.Applet.__init__(self)

        self.log = Log("budgie-browser-profile-launcher")
        self.localStateHelper = LocalStateHelper()
        self.popenHelper = PopenHelper()
        self.sortHelper = SortHelper()

        self.buildIndicator()
        self.buildPopover()
        self.buildStack()

        self.update(True)


    ####################################
    # build START
    ####################################
    def buildIndicator(self):
        self.indicatorBox = Gtk.EventBox()
        self.indicatorIcon = Gtk.Image.new_from_icon_name("browser-profile-launcher-1-symbolic", Gtk.IconSize.MENU)
        self.indicatorBox.add(self.indicatorIcon)
        self.indicatorBox.connect("button-press-event", self.indicatorBoxOnPress)
        self.indicatorBox.show_all()
        self.add(self.indicatorBox)

    def buildPopover(self):
        self.popover = Budgie.Popover.new(self.indicatorBox)
        self.popover.set_default_size(self.popoverWidth, self.popoverHeight)

    def buildStack(self):
        self.stack = Gtk.Stack()
        self.stack.set_homogeneous(False)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.popover.add(self.stack)

        ## page 1
        page1 = Gtk.Box(Gtk.Orientation.VERTICAL, 0)
        page1.border_width = 0
        page1.get_style_context().add_class("budgie-menu")
        self.stack.add_named(page1, "page1")
        # page1.props.valign = Gtk.Align.START

        ## page 1 listview
        self.listView = ListView(4)
        self.listView.setMaxMinHeights(self.popoverMaxHeight, self.popoverMinHeight)
        self.listView.setMargins(10, 3, 0, 0)
        # self.listView.get_style_context().add_class("budgie-menu")
        page1.pack_start(self.listView, False, False, 0)

        ## page 2
        page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page2.border_width = 0
        # page2.props.valign = Gtk.Align.START
        self.setMargin(page2, 10, 3, 3, 3)
        self.stack.add_named(page2, "page2")

        ## page 2 inner Box 1
        page2InnerBox1 = Gtk.HBox()
        page2InnerBox1.props.valign = Gtk.Align.START
        page2InnerBox1.props.halign = Gtk.Align.START
        page2.pack_start(page2InnerBox1, False, True, 0)

        ## page 2 inner Box 1 content
        backButton = DirectionalButton(" Back", Gtk.PositionType.LEFT);
        backButton.connect("clicked", self.backButtonOnClick)
        page2InnerBox1.add(backButton)

        ## page 2 dialog
        self.dialog = Dialog()
        page2.pack_start(self.dialog, True, True, 0)
        # self.dialog.setTitle("Delete Profile 1?")
        # self.dialog.setSubTitle("Chromium will close.")
        self.dialog.addOnClickMethodToNoBtn(self.dialogNoButtonOnClick)
        self.dialog.addOnClickMethodToYesBtn(self.dialogYesButtonOnClick)

    def buildListItemWithBrowserName(self, browser, sectionNum):

        listItem = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.listView.addItem(listItem, sectionNum)

        label = Gtk.Label(browser.getName(), xalign=0)
        label.set_margin_left(8)
        label.get_style_context().add_class("dim-label")
        listItem.pack_start(label, True, True, 0)

        addNewProfileButton = BrowserButton(browser, "browser-profile-launcher-add-new-symbolic", "Add new person")
        listItem.pack_end(addNewProfileButton, False, False, 0)
        addNewProfileButton.connect("clicked", self.addNewProfileButtonOnClick)

        if browser.getKey() is Browser.KEY_CHROMIUM:
            newTempProfileButton = BrowserButton(browser, "browser-profile-launcher-butterfly-symbolic", "New temp window")
            listItem.pack_end(newTempProfileButton, False, False, 0)
            newTempProfileButton.connect("clicked", self.newTempProfileButtonOnClick)

    def buildListItemWithProfile(self, profile, sectionNum):
        listItem = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.listView.addItem(listItem, sectionNum)

        launcherButton = LauncherButton(profile, self.popoverWidth, self.launcherButtonHeight)
        listItem.pack_start(launcherButton, True, True, 0)
        launcherButton.connect("clicked", self.launcherButtonOnClick)
        self.launcherButtons.append(launcherButton)

        deleteButton = ProfileButton(profile, "browser-profile-launcher-delete-symbolic", "Delete person")
        listItem.pack_end(deleteButton, False, False, 0)
        # deleteButton.get_style_context().add_class("destructive-action")
        deleteButton.connect("clicked", self.deleteButtonOnClick)

        incognitoButton = ProfileButton(profile, "browser-profile-launcher-incognito-symbolic", "New incognito window")
        listItem.pack_end(incognitoButton, False, False, 0)
        incognitoButton.connect("clicked", self.incognitoButtonOnClick)
    ####################################
    # build END
    ####################################


    ####################################
    # OnClick START
    ####################################
    def backButtonOnClick(self, widget):
        self.stack.set_visible_child_name("page1")

    def dialogNoButtonOnClick(self, btn):
        self.stack.set_visible_child_name("page1")

    def dialogYesButtonOnClick(self, btn):
        self.deleteProfile(self.currentProfile)
        self.update(False)
        self.stack.set_visible_child_name("page1")

    def newTempProfileButtonOnClick(self, button):
        self.currentBrowser = button.getBrowser()
        self.hidePopover()
        self.popenHelper.launchNewTempWindow(button.getBrowser())

    def addNewProfileButtonOnClick(self, button):
        self.hidePopover()
        profileKey = self.localStateHelper.getNewProfileKey(button.getBrowser())
        self.popenHelper.addNewProfile(button.getBrowser(), profileKey)

    def backButtonOnClick(self, button):
        self.stack.set_visible_child_name("page1")

    def incognitoButtonOnClick(self, button):
        self.currentProfile = button.getProfile()
        self.currentBrowser = button.getProfile().getBrowser()
        self.hidePopover()
        self.popenHelper.launchNewInconitoWindow(button.getProfile())

    def deleteButtonOnClick(self, button):
        self.currentProfile = button.getProfile()
        self.currentBrowser = button.getProfile().getBrowser()
        self.stack.set_visible_child_name("page2")
        self.dialog.setTitle("Delete %s?" % button.getProfile().getProfileName())
        self.dialog.setSubTitle("%s will close." % button.getProfile().getBrowser().getName())

    def launcherButtonOnClick(self, button):
        self.currentProfile = button.getProfile()
        self.currentBrowser = button.getProfile().getBrowser()
        self.hidePopover()
        self.popenHelper.launchBrowserProfile(self.currentProfile)
    ####################################
    # OnClick END
    ####################################


    ####################################
    # OnPess START
    ####################################
    def indicatorBoxOnPress(self, box, e):
        self.stack.set_visible_child_name("page1")
        if e.button != 1:
            return Gdk.EVENT_PROPAGATE
        if self.popover.get_visible():
            self.popover.hide()
        else:
            self.update(True)
            self.manager.show_popover(self.indicatorBox)
        return Gdk.EVENT_STOP
    ####################################
    # OnPess END
    ####################################


    ####################################
    # update START
    ####################################
    def update(self, isListItemAdded):
        # self.log.d(self.TAG, "update")
        self.listView.clean(2)
        self.listView.clean(4)
        self.launcherButtons = []
        self.lenProfiles = 0
        self.updateChromiumSections()
        self.updateChromeSections()
        if isListItemAdded:
            self.onScrollWindowChildAdd()
        else:
            self.onScrollWindowChildRemove()
        self.popover.get_child().show_all()
        self.show_all()

    def updateChromiumSections(self):
        # self.log.d(self.TAG, "updateChromiumSections")
        if self.localStateHelper.isChromiumAvailable():
            if self.listView.isEmtpy(1):
                self.chromiumBrowser = Browser(Browser.CHROMIUM)
                self.availableBrowsers.append(self.chromiumBrowser)
                self.buildListItemWithBrowserName(self.chromiumBrowser, 1)

            chromiumProfiles = self.localStateHelper.getChromiumProfiles()
            chromiumProfiles = self.sortHelper.sortedProfiles(chromiumProfiles)
            self.lenProfiles += len(chromiumProfiles)
            for profile in chromiumProfiles:
                # self.log.d(self.TAG, "updateChromiumSections person : %s, profile : %s" % (profile.getProfileName(), profile.getProfileKey()))
                self.buildListItemWithProfile(profile, 2)
        else:
            self.listView.clean(1)
            self.chromiumBrowser = None

    def updateChromeSections(self):
        # self.log.d(self.TAG, "updateChromeSections")
        if self.localStateHelper.isChromeAvailable():
            if self.listView.isEmtpy(3):
                self.chromeBrowser = Browser(Browser.CHROME)
                self.availableBrowsers.append(self.chromeBrowser)
                self.buildListItemWithBrowserName(self.chromeBrowser, 3)
            chromeProfiles = self.localStateHelper.getChromeProfiles()
            chromeProfiles = self.sortHelper.sortedProfiles(chromeProfiles)
            self.lenProfiles += len(chromeProfiles)
            for profile in chromeProfiles:
                # self.log.d(self.TAG, "updateChromeSections person : %s, profile : %s" % (profile.getProfileName(), profile.getProfileKey()))
                self.buildListItemWithProfile(profile, 4)
        else:
            self.listView.clean(3)
            self.chromeBrowser = None

    ## This is a virtual method of the Budgie.Applet
    ## https://lazka.github.io/pgi-docs/Budgie-1.0/classes/Applet.html#Budgie.Applet.do_update_popovers
    def do_update_popovers(self, manager):
        self.manager = manager
        self.manager.register_popover(self.indicatorBox, self.popover)
    ####################################
    # update END
    ####################################


    ####################################
    # hide START
    ####################################
    def hidePopover(self):
        if (self.popover is not None):
            if self.popover.get_visible():
                self.popover.hide()
    ####################################
    # hide END
    ####################################


    ####################################
    # others START
    ####################################
    def deleteProfile(self, profile):
        # self.log.d(self.TAG, "deleteProfile")
        self.popenHelper.killBrowser(self.currentBrowser)
        self.localStateHelper.delete(profile)
        self.popenHelper.deleteDir(self.localStateHelper.getProfileConfigPath(profile))
        self.popenHelper.deleteDir(self.localStateHelper.getProfileCachePath(profile))

    def setMargin(self, widget, top, bottom, left, right):
        widget.set_margin_top(top)
        widget.set_margin_bottom(bottom)
        widget.set_margin_left(left)
        widget.set_margin_right(right)
    ####################################
    # others END
    ####################################


    ####################################
    # onScrollWindowChild START
    ####################################
    def onScrollWindowChildAdd(self):
        height1 = self.listView.getHeight()
        # height2 = self.popover.get_allocated_height()
        height2 = self.listView.getHeight2()
        height = max([height1, height2])

        # print("onScrollWindowChildAdd height1 : %s" % height1)
        # print("onScrollWindowChildAdd height2 : %s" % height2)
        # print("onScrollWindowChildAdd height : %s" % height)

        self.listView.onResize(height)

        if height >= self.popoverMaxHeight:
            self.popover.resize(self.popoverMinWidth, self.popoverMaxHeight)
        elif height < self.popoverMaxHeight:
            self.popover.resize(self.popoverMinWidth, height)

        self.popover.get_child().show_all()
        self.show_all()

    def onScrollWindowChildRemove(self):
        height1 = self.listView.getHeight()
        # height2 = self.popover.get_allocated_height()
        height2 = self.listView.getHeight2()
        height = min([height1, height2])

        # print("onScrollWindowChildRemove height1 : %s" % height1)
        # print("onScrollWindowChildRemove height2 : %s" % height2)
        # print("onScrollWindowChildRemove height : %s" % height)

        self.listView.onResize(height)

        if height >= self.popoverMaxHeight:
            self.popover.resize(self.popoverMinWidth, self.popoverMaxHeight)
        elif height < self.popoverMaxHeight:
            self.popover.resize(self.popoverMinWidth, height)

        self.popover.get_child().show_all()
        self.show_all()
    ####################################
    # onScrollWindowChild END
    ####################################