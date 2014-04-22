__author__ = 'Hossein Noroozpour'
from gi.repository import Gtk
from HGEAddWindow import AddWindow
from HGETerrainWindow import TerrainWindow


class ToolBar(Gtk.ScrolledWindow):
    """ToolBar for HGE main window."""
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        self.set_min_content_height(60)

        self.m_tool_bar_file_new = Gtk.Button()
        self.m_tool_bar_file_new_image = Gtk.Image()
        self.m_tool_bar_file_new_image.set_from_file('resources/new.png')
        self.m_tool_bar_file_new.set_image(self.m_tool_bar_file_new_image)
        self.m_tool_bar_file_new.set_tooltip_text('New Scene')

        self.m_tool_bar_file_add = Gtk.Button()
        self.m_tool_bar_file_add_image = Gtk.Image()
        self.m_tool_bar_file_add_image.set_from_file('resources/add.png')
        self.m_tool_bar_file_add.set_image(self.m_tool_bar_file_add_image)
        self.m_tool_bar_file_add.connect('clicked', self.on_add_click)
        self.m_tool_bar_file_add.set_tooltip_text('Add Object')

        self.m_tool_bar_file_open = Gtk.Button()
        self.m_tool_bar_file_open_image = Gtk.Image()
        self.m_tool_bar_file_open_image.set_from_file('resources/open.png')
        self.m_tool_bar_file_open.set_image(self.m_tool_bar_file_open_image)
        self.m_tool_bar_file_open.set_tooltip_text('Open Scene')

        self.m_tool_bar_file_quit = Gtk.Button()
        self.m_tool_bar_file_quit_image = Gtk.Image()
        self.m_tool_bar_file_quit_image.set_from_file('resources/quit.png')
        self.m_tool_bar_file_quit.set_image(self.m_tool_bar_file_quit_image)
        self.m_tool_bar_file_quit.set_tooltip_text('Quit')

        self.m_tool_bar_terrain = Gtk.Button()
        self.m_tool_bar_terrain_image = Gtk.Image()
        self.m_tool_bar_terrain_image.set_from_file('resources/terrain.png')
        self.m_tool_bar_terrain.set_image(self.m_tool_bar_terrain_image)
        self.m_tool_bar_terrain.connect('clicked', self.on_terrain_click)
        self.m_tool_bar_terrain.set_tooltip_text('Terrain Settings')

        self.m_tool_bar_grid = Gtk.Grid()
        self.add(self.m_tool_bar_grid)
        self.m_tool_bar_grid.set_vexpand(False)
        self.m_tool_bar_grid.set_hexpand(False)
        self.m_tool_bar_grid.attach(self.m_tool_bar_file_new, 0, 0, 1, 1)
        self.m_tool_bar_grid.attach(self.m_tool_bar_file_add, 1, 0, 1, 1)
        self.m_tool_bar_grid.attach(self.m_tool_bar_file_open, 2, 0, 1, 1)
        self.m_tool_bar_grid.attach(self.m_tool_bar_file_quit, 3, 0, 1, 1)
        self.m_tool_bar_grid.attach(self.m_tool_bar_terrain, 4, 0, 1, 1)

        self.add_window = None

    def on_add_click(self, widget):
        self.add_window = AddWindow()

    def on_terrain_click(self, widget):
        self.terrain_window = TerrainWindow()