import threading

from gi.repository import Gtk


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

        if filename:
            def do_import():
                self._window.import_button.set_sensitive(False)
                self._window.progress.set_fraction(0)
                self._window.header_bar.pack_start(self._window.progress)
                self._window.show_all()

                def imported(photo_hash, percent):
                    self._window.progress.set_fraction(percent)
                    self._window.selection = self._window.library.update(
                        self._window.selection)

                def notify_progress(photo_name):
                    self._window.progress.set_text(photo_name)

                self._window.library.import_photos(
                    filename, notify=notify_progress, imported=imported)

                self._window.import_button.set_sensitive(True)
                self._window.header_bar.remove(self._window.progress)

            thread = threading.Thread(target=do_import)
            thread.daemon = True
            thread.start()

        self.destroy()
