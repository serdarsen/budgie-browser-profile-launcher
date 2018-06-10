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


class LauncherButton(Gtk.Button):

    def __init__(self, profile, width, height):

        Gtk.Button.__init__(self)

        self.TAG = "LauncherButton"
        # self.set_tooltip_text(profile.getProfileKey())
        self.set_can_focus(False);
        self.set_size_request(width, height)
        self.border_width = 0
        self.get_style_context().add_class("flat")
        self.profile = profile

        content = Gtk.Box(Gtk.Orientation.HORIZONTAL, 0)
        self.add(content)

        icon = Gtk.Image.new_from_icon_name("browser-profile-launcher-2-symbolic", Gtk.IconSize.MENU)
        content.pack_start(icon, False, False, 0)

        label = Gtk.Label(self.profile.getProfileName(), xalign=0)
        content.pack_start(label, True, True, 0)
        label.set_margin_left(8)

    def getProfile(self):
        return self.profile
