__author__ = 'Hossein Noroozpour'
import gc
from gi.repository import Gtk
from utility.HGEColladaImporter import collada_importer


class AddWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Add window')

        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.m_grid = Gtk.Grid()
        self.add(self.m_grid)

        self.m_collada_radio = Gtk.RadioButton.new_with_label_from_widget(None, 'Add from Collada file')
        self.m_collada_radio.connect('clicked', self.on_collada_radio_clicked)
        self.m_grid.attach(self.m_collada_radio, 0, 0, 1, 1)

        self.m_hge_radio = Gtk.RadioButton.new_with_label_from_widget(self.m_collada_radio, 'Add from HGE file')
        self.m_hge_radio.connect('clicked', self.on_hge_radio_clicked)
        self.m_grid.attach(self.m_hge_radio, 0, 1, 1, 1)

        self.m_collada_filter = Gtk.FileFilter()
        self.m_collada_filter.add_pattern('*.[Dd][Aa][Ee]')

        self.m_collada_file_button = Gtk.FileChooserButton('Select your Collada file', Gtk.FileChooserAction.OPEN)
        self.m_collada_file_button.set_filter(self.m_collada_filter)
        self.m_collada_file_button.connect('file-set', self.on_collada_file_button_file_set)
        self.m_grid.attach(self.m_collada_file_button, 0, 2, 1, 1)

        self.m_hge_filter = Gtk.FileFilter()
        self.m_hge_filter.add_pattern('*.[Hh][Gg][Ee]')

        self.m_hge_file_button = Gtk.FileChooserButton('Select your HGE file', Gtk.FileChooserAction.OPEN)
        self.m_hge_file_button.set_filter(self.m_hge_filter)
        self.m_hge_file_button.connect('file-set', self.on_hge_file_button_file_set)
        self.m_grid.attach(self.m_hge_file_button, 0, 3, 1, 1)

        self.m_add_button = Gtk.Button('Add Collada file')
        self.m_add_button.connect('clicked', self.on_add_click)
        self.m_grid.attach(self.m_add_button, 0, 4, 1, 1)

        self.show_all()

        self.m_add_button.hide()
        self.m_hge_file_button.hide()

    def on_collada_radio_clicked(self, widget):
        """Click on Collada radio button"""
        self.m_hge_file_button.hide()
        self.m_collada_file_button.show()
        self.m_add_button.set_label('Add Collada file')
        if len(self.m_collada_file_button.get_filenames()) == 0:
            self.m_add_button.hide()
        else:
            self.m_add_button.show()

    def on_hge_radio_clicked(self, widget):
        """Click on HGE radio button"""
        self.m_collada_file_button.hide()
        self.m_hge_file_button.show()
        self.m_add_button.set_label('Add HGE file')
        if len(self.m_hge_file_button.get_filenames()) == 0:
            self.m_add_button.hide()
        else:
            self.m_add_button.show()

    def on_collada_file_button_file_set(self, widget):
        """Collada file set."""
        if self.m_collada_radio.get_active():
            self.m_add_button.show()
        else:
            self.m_add_button.hide()

    def on_hge_file_button_file_set(self, widget):
        """HGE file set."""
        if self.m_hge_radio.get_active():
            self.m_add_button.show()
        else:
            self.m_add_button.hide()

    def on_add_click(self, widget):
        """Add clicked"""
        if self.m_collada_radio.get_active() and len(self.m_collada_file_button.get_filenames()) != 0:
            files = self.m_collada_file_button.get_filenames()
            actors = []
            for f in files:
                actors = actors + ColladaToHGEActors(f)
            gc.collect()
        elif self.m_hge_radio.get_active() and len(self.m_hge_file_button.get_filenames()) != 0:
            #todo
            pass
