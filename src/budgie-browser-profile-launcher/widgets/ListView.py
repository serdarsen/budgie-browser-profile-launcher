#!/usr/bin/python3

# This file is part of Browser Profile Launcher

# Copyright © 2018 Serdar ŞEN <serdarbote@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


import gi.repository
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ListView(Gtk.ScrolledWindow):

    def __init__(self, childSectionsNum):

        self.rootSection = None
        self.childSections = {}
        self.margins = [0, 0, 0, 0]  # top, bottom, left, right

        Gtk.ScrolledWindow.__init__(self)

        self.TAG = "ListView"
        self.set_overlay_scrolling(True)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.buildSections(childSectionsNum)

    def setMargins(self, top, bottom, left, right):
        self.margins = [top, bottom, left, right]
        self.set_margin_top(top)
        self.set_margin_bottom(bottom)
        self.set_margin_left(left)
        self.set_margin_right(right)

    def getMargins(self):
        return self.margins

    def getMarginTop(self):
        return self.margins[0]

    def getMarginBottom(self):
        return self.margins[1]

    def buildSections(self, num):

        self.rootSection = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.rootSection.border_width = 0
        self.add(self.rootSection)
        for i in range(1, num + 1):
            # section = Gtk.VBox()
            section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            section.border_width = 0
            section.props.valign = Gtk.Align.START
            self.rootSection.add(section)
            self.childSections[i] = section


    def addItem(self, item, sectionNum):
        childSection = self.childSections[sectionNum]
        childSection.add(item)

    def cleanRootSection(self):
        if self.rootSection.get_children() is not None:
            for child in self.rootSection.get_children():
                self.rootSection.remove(child)

    def clean(self, sectionNum):
        childSection = self.childSections[sectionNum]
        if childSection.get_children() is not None:
            for child in childSection.get_children():
                childSection.remove(child)

    def isEmtpy(self, sectionNum):
        childSection = self.childSections[sectionNum]
        children = childSection.get_children()
        if children is not None:
            if len(children) > 0:
                return False
            else:
                return True


    # def scrollToBottom(self):
    #     adjustment = self.get_vadjustment()
    #     print("adjustment.get_upper() %s " + adjustment.get_upper())
    #     print("adjustment.get_page_size() %s " + adjustment.get_page_size())
    #     adjustment.set_value(adjustment.get_upper() - adjustment.get_page_size())