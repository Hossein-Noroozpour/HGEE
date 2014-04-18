__author__ = """Hossein Noroozpour"""

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from time import time

class ProfilerWindow(Gtk.ScrolledWindow):
    """Scrolled Window for profiler page in side tab in main window"""
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.m_profiler_grid = Gtk.Grid()
        self.m_profiler_grid.set_hexpand(True)
        self.m_profiler_grid.set_vexpand(True)

        self.add(self.m_profiler_grid)

        self.m_frame_rate_text = Gtk.Label()
        self.m_frame_rate_text.set_text("FRPS")
        self.m_frame_rate_text.set_hexpand(True)
        self.m_frame_rate_text.set_vexpand(False)
        self.m_frame_rate_text.set_halign(1)
        self.m_frame_rate_text.set_valign(1)

        self.m_frame_rate_label = Gtk.Label()
        self.m_frame_rate_label.set_hexpand(True)
        self.m_frame_rate_label.set_vexpand(False)
        self.m_frame_rate_label.set_halign(1)
        self.m_frame_rate_label.set_valign(1)

        self.m_profiler_grid.attach(self.m_frame_rate_text, 0, 0, 1, 1)
        self.m_profiler_grid.attach(self.m_frame_rate_label, 1, 0, 1, 1)

        self.m_time = time()
        self.m_frame_rate = 0.0

    def one_frame_passed(self):
        self.m_frame_rate += 1.0
        if time() > self.m_time + 1.0:
            self.m_frame_rate /= (time() - self.m_time)
            self.m_frame_rate_label.set_text(str(self.m_frame_rate))
            self.m_frame_rate = 0.0
            self.m_time = time()