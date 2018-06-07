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
        self.popoverHeightOffset = 36 + 20
        self.popoverMinHeight = 150
        self.popoverMaxHeight = 480
        self.popoverHeight = 0
        self.popoverWidth = 270
        self.launcherButtonHeight = 36
        self.lenProfiles = 0
        self.launcherButtons = []
        self.availableBrowsers = []
        self.currentProfile = None
        self.currentBrowser = None
        self.chromiumBrowser = None
        self.chromeBrowser = None
        self.currentLauncherRevealer = None
        self.chromiumRevealer = None
        self.chromeRevealer = None

        Budgie.Applet.__init__(self)

        self.log = Log("budgie-browser-profile-launcher")
        self.localStateHelper = LocalStateHelper()
        self.popenHelper = PopenHelper()
        self.sortHelper = SortHelper()

        self.buildIndicator()
        self.buildPopover()
        self.buildStack()

        self.update()


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
        self.stack.set_homogeneous(True)
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

    def buildListItemWithBrowserName(self, revealerButtonOnClick, browser, sectionNum):

        listItem = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        revealerButton = Gtk.Button()
        label = Gtk.Label(browser.getName(), xalign=0)
        revealerButton.add(label)
        revealerButton.set_can_focus(False);
        revealerButton.set_size_request(self.popoverWidth, 0)
        listItem.add(revealerButton)
        self.listView.addItem(listItem, sectionNum)
        revealerButton.get_style_context().add_class("flat");
        revealerButton.connect('button-press-event', revealerButtonOnClick)

        revealer = Gtk.Revealer()
        listItem.add(revealer)
        topRevealerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        topRevealerBox.props.halign = Gtk.Align.START
        # self.setMargin(topRevealerBox, 0, 10, 0, 0)
        revealer.add(topRevealerBox)
        revealer.set_reveal_child(False)

        if browser.getKey() is Browser.KEY_CHROMIUM:
            newTempProfileButton = Gtk.Button()
            newTempProfileImage = Gtk.Image.new_from_icon_name("browser-profile-launcher-butterfly-symbolic",
                                                               Gtk.IconSize.MENU)
            newTempProfileButton.add(newTempProfileImage)
            newTempProfileButton.set_tooltip_text("New temp window")
            newTempProfileButton.set_can_focus(False);
            topRevealerBox.add(newTempProfileButton)
            newTempProfileButton.get_style_context().add_class("flat")
            newTempProfileButton.connect("clicked", self.newTempProfileButtonOnClick)

        addNewProfileButton = Gtk.Button()
        addNewProfileImage = Gtk.Image.new_from_icon_name("browser-profile-launcher-add-new-symbolic",
                                                          Gtk.IconSize.MENU)
        addNewProfileButton.add(addNewProfileImage)
        addNewProfileButton.set_tooltip_text("Add new person")
        addNewProfileButton.set_can_focus(False);
        topRevealerBox.add(addNewProfileButton)
        addNewProfileButton.get_style_context().add_class("flat")
        addNewProfileButton.connect("clicked", self.addNewProfileButtonOnClick)

        return revealer

    def buildListItemWithProfile(self, profile, sectionNum):

        listItem = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        launcherButton = LauncherButton(profile, self.popoverWidth, self.launcherButtonHeight)
        self.launcherButtons.append(launcherButton)

        listItem.add(launcherButton)
        self.listView.addItem(listItem, sectionNum)
        launcherButton.connect("button-press-event", self.launcherButtonOnPress)

        laucherRevealer = Gtk.Revealer()
        listItem.add(laucherRevealer)
        laucherRevealerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        laucherRevealerBox.props.halign = Gtk.Align.START
        # self.setMargin(laucherRevealerBox, 0, 10, 0, 0)
        laucherRevealer.add(laucherRevealerBox)
        laucherRevealer.set_reveal_child(False)
        launcherButton.setRevealer(laucherRevealer)

        incognitoButton = Gtk.Button()
        incognitoButton.set_tooltip_text("New incognito window")
        incognitoImage = Gtk.Image.new_from_icon_name("browser-profile-launcher-incognito-symbolic", Gtk.IconSize.MENU)
        incognitoButton.add(incognitoImage)
        incognitoButton.set_can_focus(False);
        laucherRevealerBox.add(incognitoButton)
        incognitoButton.get_style_context().add_class("flat");
        incognitoButton.connect("clicked", self.incognitoButtonOnClick)

        deleteButton = Gtk.Button()
        deleteButton.set_tooltip_text("Delete person")
        deleteImage = Gtk.Image.new_from_icon_name("browser-profile-launcher-delete-symbolic", Gtk.IconSize.MENU)
        deleteButton.add(deleteImage)
        deleteButton.set_can_focus(False);
        laucherRevealerBox.add(deleteButton)
        deleteButton.get_style_context().add_class("flat")
        deleteButton.get_style_context().add_class("destructive-action")
        deleteButton.connect("clicked", self.deleteButtonOnClick)

    ####################################
    # build END
    ####################################


    ####################################
    # OnClick START
    ####################################
    def backButtonOnClick(self, widget):
        self.stack.set_visible_child_name("page1")

    def dialogNoButtonOnClick(self, btn):
        self.hideCurrentLaucherRevealer()
        self.stack.set_visible_child_name("page1")

    def dialogYesButtonOnClick(self, btn):
        self.deleteProfile(self.currentProfile)
        self.update()
        self.stack.set_visible_child_name("page1")

    def newTempProfileButtonOnClick(self, widget):
        self.hidePopover()
        self.hideAllRevealers()
        self.popenHelper.launchNewTempWindow(self.currentBrowser)

    def addNewProfileButtonOnClick(self, widget):
        self.hidePopover()
        self.hideAllRevealers()
        profileKey = self.localStateHelper.getNewProfileKey(self.currentBrowser)
        self.popenHelper.addNewProfile(self.currentBrowser, profileKey)

    def backButtonOnClick(self, button):
        self.stack.set_visible_child_name("page1")

    ## Launches browser profile
    def incognitoButtonOnClick(self, button):
        self.hidePopover()
        self.popenHelper.launchNewInconitoWindow(self.currentProfile)
        self.hideCurrentLaucherRevealer()

    def deleteButtonOnClick(self, button):
        self.stack.set_visible_child_name("page2")
        self.dialog.setTitle("Delete %s?" % self.currentProfile.getProfileName())
        self.dialog.setSubTitle("%s will close." % self.currentBrowser.getName())
    ####################################
    # OnClick END
    ####################################


    ####################################
    # OnPess START
    ####################################
    def indicatorBoxOnPress(self, box, e):
        self.stack.set_visible_child_name("page1")
        self.hideAllRevealers()
        if e.button != 1:
            return Gdk.EVENT_PROPAGATE
        if self.popover.get_visible():
            self.popover.hide()
        else:
            self.update()
            self.manager.show_popover(self.indicatorBox)
        return Gdk.EVENT_STOP

    def chromiumRevealerButtonOnPress(self, button, event):
        self.currentBrowser = self.chromiumBrowser
        self.hideAllLauncherButtonRevealers()
        self.hideChromeRevealer()
        reveal = self.chromiumRevealer.get_reveal_child()
        self.chromiumRevealer.set_reveal_child(not reveal)

    def chromeRevealerButtonOnPress(self, button, event):
        self.currentBrowser = self.chromeBrowser
        self.hideAllLauncherButtonRevealers()
        self.hideChromiumRevealer()
        reveal = self.chromeRevealer.get_reveal_child()
        self.chromeRevealer.set_reveal_child(not reveal)

    ## listens menu button clicks
    def launcherButtonOnPress(self, button, event):
        self.currentLauncherRevealer = button.getRevealer()
        self.currentProfile = button.getProfile()
        self.currentBrowser = self.currentProfile.getBrowser()
        ## Left Mouse Button OnClick
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            self.hidePopover()
            self.hideAllRevealers()
            self.popenHelper.launchBrowserProfile(self.currentProfile)
        ## Right Mouse Button OnClick
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.hideAllBrowserRevealers()
            menuRevealer = button.getRevealer()
            reveal = menuRevealer.get_reveal_child()
            menuRevealer.set_reveal_child(not reveal)
            self.hideAllLauncherButtonRevealersExceptThis(button)
    ####################################
    # OnPess END
    ####################################


    ####################################
    # update START
    ####################################
    def update(self):
        # self.log.d(self.TAG, "update")
        self.listView.clean(2)
        self.listView.clean(4)
        self.launcherButtons = []
        self.lenProfiles = 0
        self.updateChromiumSections()
        self.updateChromeSections()
        self.resizePopover()
        self.popover.get_child().show_all()
        self.show_all()

    def updateChromiumSections(self):
        # self.log.d(self.TAG, "updateChromiumSections")
        if self.localStateHelper.isChromiumAvailable():
            if self.listView.isEmtpy(1):
                self.chromiumBrowser = Browser(Browser.CHROMIUM)
                self.availableBrowsers.append(self.chromiumBrowser)
                self.chromiumRevealer = self.buildListItemWithBrowserName(self.chromiumRevealerButtonOnPress, self.chromiumBrowser, 1)

            chromiumProfiles = self.localStateHelper.getChromiumProfiles()
            chromiumProfiles = self.sortHelper.sortedProfiles(chromiumProfiles)
            self.lenProfiles += len(chromiumProfiles)
            for profile in chromiumProfiles:
                # self.log.d(self.TAG, "updateChromiumSections person : %s, profile : %s" % (profile.getProfileName(), profile.getProfileKey()))
                self.buildListItemWithProfile(profile, 2)
        else:
            self.listView.clean(1)
            self.chromiumBrowser = None
            self.chromiumBrowser = None

    def updateChromeSections(self):
        # self.log.d(self.TAG, "updateChromeSections")
        if self.localStateHelper.isChromeAvailable():
            if self.listView.isEmtpy(3):
                self.chromeBrowser = Browser(Browser.CHROME)
                self.availableBrowsers.append(self.chromeBrowser)
                self.chromeRevealer = self.buildListItemWithBrowserName(self.chromeRevealerButtonOnPress, self.chromeBrowser, 3)
            chromeProfiles = self.localStateHelper.getChromeProfiles()
            chromeProfiles = self.sortHelper.sortedProfiles(chromeProfiles)
            self.lenProfiles += len(chromeProfiles)
            for profile in chromeProfiles:
                # self.log.d(self.TAG, "updateChromeSections person : %s, profile : %s" % (profile.getProfileName(), profile.getProfileKey()))
                self.buildListItemWithProfile(profile, 4)
        else:
            self.listView.clean(3)
            self.chromeBrowser = None
            self.chromeRevealer = None

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
    def hideAllRevealers(self):
        self.hideAllBrowserRevealers()
        self.hideAllLauncherButtonRevealers()

    def hideAllBrowserRevealers(self):
        self.hideChromiumRevealer()
        self.hideChromeRevealer()

    def hideChromeRevealer(self):
        if self.chromeRevealer is not None:
            self.chromeRevealer.set_reveal_child(False)

    def hideChromiumRevealer(self):
        if self.chromiumRevealer is not None:
            self.chromiumRevealer.set_reveal_child(False)

    def hideAllLauncherButtonRevealers(self):
        for btn in self.launcherButtons:
            btn.getRevealer().set_reveal_child(False)

    def hideAllLauncherButtonRevealersExceptThis(self, button):
        for btn in self.launcherButtons:
            if btn is not button:
                btn.getRevealer().set_reveal_child(False)

    def hideCurrentLaucherRevealer(self):
        if self.currentLauncherRevealer is not None:
            self.currentLauncherRevealer.set_reveal_child(False)

    # hides popover if it is visible
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
    def resizePopover(self):
        profilesLenght = self.lenProfiles
        browsersLenght = len(self.availableBrowsers)
        listItemsLenght = browsersLenght + profilesLenght

        self.popoverHeight = self.launcherButtonHeight * listItemsLenght + self.listView.getMarginTop() + self.listView.getMarginBottom() + self.popoverHeightOffset

        if self.popoverHeight > self.popoverMaxHeight:
            self.popoverHeight = self.popoverMaxHeight
        if self.popoverHeight < self.popoverMinHeight:
            self.popoverHeight = self.popoverMinHeight

        self.popover.resize(self.popoverWidth, self.popoverHeight)

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

    # def getSizes(self):
    #     if len(self.launcherButtons) > 0:
    #         lBtn = self.launcherButtons[0]
    #         self.log.d(self.TAG, "lBtnHeight : %s" % lBtn.get_allocation().height)
    #         if lBtn.get_allocation().height > 1:
    #             self.launcherButtonHeight = lBtn.get_allocation().height
    #             self.popoverHeightOffset = lBtn.get_allocation().height
    #             self.listViewButtonOffset = 0
    ####################################
    # others END
    ####################################