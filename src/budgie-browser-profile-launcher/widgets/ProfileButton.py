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


class ProfileButton(Gtk.Button):

    def __init__(self, profile, iconName, toolTipText):
        Gtk.Button.__init__(self)
        self.profile = profile
        self.border_width = 0
        self.set_can_focus(False)
        self.set_tooltip_text(toolTipText)
        self.get_style_context().add_class("flat")
        self.image = Gtk.Image.new_from_icon_name(iconName, Gtk.IconSize.MENU)
        self.add(self.image)

    def setProfile(self, profile):
        self.profile = profile

    def getProfile(self):
        return self.profile