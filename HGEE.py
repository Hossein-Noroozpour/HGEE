# coding=utf-8
"""
Main module for HGEE (Hulixerian Game Engine Editor)
"""
__author__ = """Hossein Noroozpour"""
from ui.HGEOpenGLRenderingArea import OpenGLRenderingArea
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from ui.HGESideTab import SideTab
from core.HGEApplication import Application


class MainWindow(Gtk.Window):
    """MainWindow class for Editor"""

    def __init__(self):
        Gtk.Window.__init__(self, title="Hulixerian Game Engine Editor")

        self.set_default_size(700, 500)
        self.set_position(1)

        self.m_menu_item_file = Gtk.MenuItem()
        self.m_menu_item_file.set_label("_File")
        self.m_menu_item_file.set_use_underline(True)

        self.m_menu_item_file_new = Gtk.MenuItem()
        self.m_menu_item_file_new.set_label("_New")
        self.m_menu_item_file_new.set_use_underline(True)

        self.m_menu_item_file_open = Gtk.MenuItem()
        self.m_menu_item_file_open.set_label("_Open")
        self.m_menu_item_file_open.set_use_underline(True)

        self.m_menu_item_file_quit = Gtk.MenuItem()
        self.m_menu_item_file_quit.set_label("_Quit")
        self.m_menu_item_file_quit.set_use_underline(True)

        self.m_menu_item_file_add = Gtk.MenuItem()
        self.m_menu_item_file_add.set_label("_Add")
        self.m_menu_item_file_add.set_use_underline(True)

        self.m_menu_file = Gtk.Menu()
        self.m_menu_item_file.set_submenu(self.m_menu_file)
        self.m_menu_file.append(self.m_menu_item_file_new)
        self.m_menu_file.append(self.m_menu_item_file_open)
        self.m_menu_file.append(self.m_menu_item_file_add)
        self.m_menu_file.append(self.m_menu_item_file_quit)

        self.m_menu_item_edit = Gtk.MenuItem()
        self.m_menu_item_edit.set_label("_Edit")
        self.m_menu_item_edit.set_use_underline(True)

        self.m_menu_edit = Gtk.Menu()
        self.m_menu_item_edit.set_submenu(self.m_menu_edit)

        self.m_menu_item_help = Gtk.MenuItem()
        self.m_menu_item_help.set_label("_Help")
        self.m_menu_item_help.set_use_underline(True)

        self.m_menu_help = Gtk.Menu()
        self.m_menu_item_help.set_submenu(self.m_menu_help)

        self.m_menu_bar = Gtk.MenuBar()
        self.m_menu_bar.append(self.m_menu_item_file)
        self.m_menu_bar.append(self.m_menu_item_edit)
        self.m_menu_bar.append(self.m_menu_item_help)

        self.m_status_bar = Gtk.Statusbar()

        self.m_render_area = Gtk.DrawingArea()
        self.m_render_area_initialized = False
        self.m_render_area.connect('configure_event', self.render_area_on_configure_event)
        self.m_render_area.connect('draw', self.render_area_on_draw)
        self.m_render_area.set_double_buffered(False)
        self.m_render_area.set_hexpand(True)
        self.m_render_area.set_vexpand(True)

        m_viewport = Gtk.Grid()
        m_viewport.attach(self.m_render_area, 0, 0, 1, 1)
        m_viewport.set_hexpand(True)
        m_viewport.set_vexpand(True)

        self.m_side_tab = SideTab()

        self.m_pane_main = Gtk.Paned()
        self.m_pane_main.pack1(m_viewport, True, True)
        self.m_pane_main.pack2(self.m_side_tab, True, True)
        self.m_pane_main.set_position(500)

        self.m_grid = Gtk.Grid()
        self.m_grid.set_column_spacing(5)
        self.m_grid.set_row_spacing(5)
        self.m_grid.set_margin_top(5)
        self.m_grid.set_margin_bottom(5)
        self.m_grid.set_margin_left(5)
        self.m_grid.set_margin_right(5)
        self.add(self.m_grid)
        self.m_grid.set_vexpand(True)
        self.m_grid.set_hexpand(True)
        self.m_grid.attach(self.m_menu_bar, 0, 0, 1, 1)
        self.m_grid.attach(self.m_pane_main, 0, 1, 1, 1)
        self.m_grid.attach(self.m_status_bar, 0, 2, 1, 1)
        self.m_render_timeout = None
        self.m_render_device = None

    def initialize_render_area(self):
        """
        Initialize render area.
        """
        self.m_render_area_initialized = True
        self.m_render_device = OpenGLRenderingArea(self.m_render_area.get_window())
        self.m_render_device.set_application(Application())
        self.m_render_device.set_profiler_window(self.m_side_tab.get_profiler_window())
        self.m_render_timeout = GLib.timeout_add(18, self.m_render_device.render)

    def render_area_on_configure_event(self, widget, event):
        """Configuring Render Area
        :param event:
        :param widget:
        """
        if self.m_render_area_initialized:
            self.m_render_device.set_size(event.width, event.height)
        else:
            self.initialize_render_area()
        return True

    def render_area_on_draw(self, widget, context):
        """
        :param widget:
        :param context:
        :return:
        """
        if self.m_render_area_initialized:
            self.m_render_device.render()
        else:
            self.initialize_render_area()
        return True


if __name__ == "__main__":
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
