#!/usr/bin/env python
#
# Lara Maia <dev@lara.click> 2019
#
# The RGBFanControl is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# The RGBFanControl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from collections import OrderedDict
import utils
import config

primary_effects_dict = OrderedDict([
    ("000", "Disabled"),
    ("050", "Solid Color"),
    ("051", "Solid Color Rotating"),
    ("100", "Two Colors"),
    ("101", "Two Colors Gradient"),
    ("102", "Two Colors Up-Down"),
    ("103", "Two Colors Up-Down Oposite"),
    ("200", "Rainbow"),
    ("201", "Rainbow Rotating"),
])

secondary_effects_dict = OrderedDict([
    ("000", "Disabled"),
    ("001", "Fade"),
    ("002", "Pulse"),
])

extra_effects_dict = OrderedDict([
    ("000", "Disabled"),
    ("104", "Two Colors Random"),
    ("500", "Party"),
    ("501", "Police"),
    ("502", "RGB Cycle"),
])

extra_effect_block_list = ["050", "100", "101", "200", "201"]


class Main(Gtk.ApplicationWindow):
    def __init__(self, *, application: Gtk.Application, title: str) -> None:
        super().__init__(application=application, title=title)
        self.application = application

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)

        # icon_image = GdkPixbuf.Pixbuf.new_from_file_at_size(<image_path>, 28, 28)

        # icon = Gtk.Image()
        # icon.set_from_pixbuf(icon_image)

        # header_bar.pack_start(icon)

        menu = Gio.Menu()
        menu.append("About", "app.about")
        menu.append("Exit", "app.exit")

        menu_button = Gtk.MenuButton()
        # menu_button.set_relief(Gtk.ReliefStyle.NONE)
        menu_button.set_menu_model(menu)
        header_bar.pack_end(menu_button)

        self.set_titlebar(header_bar)
        # self.set_default_size(650, 450)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title(title)

        main_grid = Gtk.Grid()
        main_grid.set_border_width(10)
        main_grid.set_row_spacing(10)
        main_grid.set_column_spacing(10)
        main_grid.set_column_homogeneous(True)
        self.add(main_grid)

        settings_section = utils.Section("effects", "Effects")
        main_grid.attach(settings_section, 0, 0, 1, 1)

        self.primary_effect = settings_section.new(
            "primary_effect",
            "Primary Effect",
            Gtk.ComboBoxText,
            0, 0,
            items=primary_effects_dict
        )

        self.secondary_effect = settings_section.new(
            "secondary_effect",
            "Secondary Effect",
            Gtk.ComboBoxText,
            0, 1,
            items=secondary_effects_dict
        )

        self.extra_effect = settings_section.new(
            "extra_effect",
            "Extra Effect",
            Gtk.ComboBoxText,
            0, 2,
            items=extra_effects_dict
        )

        self.primary_effect.connect("changed", self.on_effects_changed)
        self.secondary_effect.connect("changed", self.on_effects_changed)
        self.extra_effect.connect("changed", self.on_effects_changed)
        self.primary_effect.load()
        self.secondary_effect.load()
        self.extra_effect.load()

        reset = Gtk.Button("Reset Arduino")
        reset.connect('clicked', self.on_reset_clicked)
        main_grid.attach(reset, 0, 1, 1, 1)

        save = Gtk.Button("EEPROM Save")
        save.connect('clicked', self.on_save_clicked)
        main_grid.attach(save, 0, 2, 1, 1)

        self.connect("destroy", self.application.on_exit_activate, None)
        self.show_all()

    def on_effects_changed(self, combo: Gtk.ComboBoxText) -> None:
        self.primary_effect.set_sensitive(True)
        self.secondary_effect.set_sensitive(True)
        name = combo.get_name()

        if name == "primary_effect":
            effect = list(primary_effects_dict)[combo.get_active()]

            if effect in extra_effect_block_list:
                self.extra_effect.set_active(0)
                self.extra_effect.set_sensitive(False)
            else:
                self.extra_effect.set_sensitive(True)
        elif name == "secondary_effect":
            effect = list(secondary_effects_dict)[combo.get_active()]
        else:
            effect = list(extra_effects_dict)[combo.get_active()]

        if self.primary_effect.get_active() == 0:
            self.secondary_effect.set_active(0)
            self.secondary_effect.set_sensitive(False)

        config.new('effects', name, effect)

        serial_message = 'le'
        serial_message += config.parser.get("effects", "extra_effect")
        serial_message += config.parser.get("effects", "secondary_effect")
        serial_message += config.parser.get("effects", "primary_effect")
        self.application.send_serial(serial_message)

    def on_reset_clicked(self, button: Gtk.Button) -> None:
        self.application.do_reset()

    def on_save_clicked(self, button: Gtk.Button) -> None:
        serial_message = 'ms'
        self.application.send_serial(serial_message)
        button.set_label("Saved!")
