import threading

from gi.repository import GLib
from gi.repository import Gtk


class ImportOptions(Gtk.Dialog):

    def __init__(self, window):
        super(ImportOptions, self).__init__(
            "Import Options",
            window,
            0,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                'Import',
                Gtk.ResponseType.OK,
            )
        )

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        copy_photo_row = Gtk.ListBoxRow()
        copy_photo_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        copy_photo_label = Gtk.Label("Copy Photos to Library", xalign=0)
        copy_photo_checkbox = Gtk.CheckButton()
        copy_photo_checkbox.set_active(True)
        copy_photo_box.pack_start(copy_photo_label, True, True, 0)
        copy_photo_box.pack_end(copy_photo_checkbox, False, True, 0)
        copy_photo_row.add(copy_photo_box)
        listbox.add(copy_photo_row)

        copy_photo_checkbox.connect('toggled', self.copy_toggled)

        self.delete_photo_row = Gtk.ListBoxRow()
        delete_photo_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        delete_photo_label = Gtk.Label(
            "Delete Originals After Import", xalign=0)
        self.delete_photo_checkbox = Gtk.CheckButton()
        delete_photo_box.pack_start(delete_photo_label, True, True, 0)
        delete_photo_box.pack_end(self.delete_photo_checkbox, False, True, 0)
        self.delete_photo_row.add(delete_photo_box)
        listbox.add(self.delete_photo_row)

        self.delete_photo_checkbox.connect('toggled', self.delete_toggled)

        box = self.get_content_area()
        box.set_spacing(3)
        box.pack_start(listbox, True, True, 0)
        box.show_all()

        self.options = {
            'copy_photos': True,
            'delete_originals': False,
        }

    def copy_toggled(self, button):
        if button.get_active():
            self.delete_photo_row.set_sensitive(True)
            self.options['copy_photos'] = True
        else:
            self.delete_photo_row.set_sensitive(False)
            self.delete_photo_checkbox.set_active(False)
            self.options['copy_photos'] = False
            self.options['delete_originals'] = False

    def delete_toggled(self, button):
        if button.get_active():
            self.options['delete_originals'] = True
        else:
            self.options['delete_originals'] = False

    def run(self):
        return (super(ImportOptions, self).run(), self.options)


class PhotoImporter(Gtk.FileChooserDialog):

    def __init__(self, window):
        super(PhotoImporter, self).__init__(
            'Choose folder to import',
            window,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                'Select',
                Gtk.ResponseType.OK,
            ),
        )

        self._window = window

    def import_photos(self):
        response = self.run()

        if response == Gtk.ResponseType.OK:
            filename = self.get_filename()
        else:
            filename = None

        dialog = ImportOptions(self)
        response = dialog.run()
        dialog.destroy()

        if filename and response[0] == Gtk.ResponseType.OK:
            def do_import():
                GLib.idle_add(self._window.import_button.set_sensitive, False)
                GLib.idle_add(self._window.progress.set_fraction, 0)
                GLib.idle_add(
                    self._window.header_bar.pack_start, self._window.progress)
                GLib.idle_add(self._window.show_all)

                def imported(photo_hash, percent):
                    GLib.idle_add(self._window.progress.set_fraction, percent)

                def notify_progress(photo_name):
                    GLib.idle_add(self._window.progress.set_text, photo_name)

                self._window.library.import_photos(
                    filename, notify=notify_progress, imported=imported)

                GLib.idle_add(self._window.import_button.set_sensitive, True)
                GLib.idle_add(
                    self._window.header_bar.remove, self._window.progress)
                GLib.idle_add(self._window.render_selection, self._window.library.update(
                    self._window.selection
                ))

            thread = threading.Thread(target=do_import)
            thread.daemon = True
            thread.start()

        self.destroy()
