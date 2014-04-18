#!/usr/bin/python3.3
__author__ = 'Hossein Noroozpour Thany Abady'
from gi.repository import Gtk
from gi.repository import cairo


class TerrainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Terrain Window')

        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.m_grid = Gtk.Grid()
        self.m_grid.set_column_spacing(5)
        self.m_grid.set_row_spacing(5)
        self.m_grid.set_margin_top(5)
        self.m_grid.set_margin_bottom(5)
        self.m_grid.set_margin_left(5)
        self.m_grid.set_margin_right(5)
        self.add(self.m_grid)

        self.m_terrain_size_label = Gtk.Label('Terrain size')
        self.m_grid.attach(self.m_terrain_size_label, 0, 1, 2, 1)

        self.m_512_size = Gtk.RadioButton.new_with_label_from_widget(None, '  512 x 512')
        self.m_grid.attach(self.m_512_size, 0, 2, 2, 1)

        self.m_1024_size = Gtk.RadioButton.new_with_label_from_widget(self.m_512_size, '1024 x 1024')
        self.m_grid.attach(self.m_1024_size, 0, 3, 2, 1)

        self.m_2048_size = Gtk.RadioButton.new_with_label_from_widget(self.m_512_size, '2048 x 2048')
        self.m_grid.attach(self.m_2048_size, 0, 4, 2, 1)

        self.m_4096_size = Gtk.RadioButton.new_with_label_from_widget(self.m_512_size, '4096 x 4096')
        self.m_grid.attach(self.m_4096_size, 0, 5, 2, 1)

        self.m_nasa_filter = Gtk.FileFilter()
        self.m_nasa_filter.add_pattern('*.[Bb][Ii][Nn]')

        self.m_nasa_file_label = Gtk.Label('NASA binary file')
        self.m_grid.attach(self.m_nasa_file_label, 0, 6, 2, 1)

        self.m_nasa_file_button = Gtk.FileChooserButton('Select the NASA binary file', Gtk.FileChooserAction.OPEN)
        self.m_nasa_file_button.set_filter(self.m_nasa_filter)
        self.m_grid.attach(self.m_nasa_file_button, 0, 7, 2, 1)

        self.m_region_horizontal_degree_label = Gtk.Label('Horizontal degree')
        self.m_grid.attach(self.m_region_horizontal_degree_label, 0, 8, 1, 1)

        self.m_region_horizontal_degree_entry = Gtk.Entry()
        self.m_grid.attach(self.m_region_horizontal_degree_entry, 1, 8, 1, 1)

        self.m_region_vertical_degree_label = Gtk.Label('Vertical degree')
        self.m_grid.attach(self.m_region_vertical_degree_label, 0, 9, 1, 1)

        self.m_region_vertical_degree_label = Gtk.Entry()
        self.m_grid.attach(self.m_region_vertical_degree_label, 1, 9, 1, 1)

        self.m_show_button = Gtk.Button('Show')
        self.m_grid.attach(self.m_show_button, 0, 10, 2, 1)

        self.m_load_button = Gtk.Button('Load')
        self.m_grid.attach(self.m_load_button, 0, 11, 2, 1)

        self.show_all()