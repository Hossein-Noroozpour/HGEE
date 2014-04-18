__author__ = """Hossein Noroozpour"""

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from HGEProfilerWindow import ProfilerWindow

class SideTab(Gtk.Notebook):
    """Side Tab in main window"""
    def __init__(self):
        Gtk.Notebook.__init__(self)

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.m_profiler_window = ProfilerWindow()

        self.m_debug_label = Gtk.Label('Profiling')

        self.append_page(self.m_profiler_window, self.m_debug_label)

    def get_profiler_window(self):
        return self.m_profiler_window