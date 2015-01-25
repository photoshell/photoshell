import os

from gi.repository import Gtk
from wand.image import Image


class PhotoExporter(Gtk.FileChooserDialog):

    def __init__(self, window):
        super(PhotoExporter, self).__init__(
            'Export photo',
            window,
            Gtk.FileChooserAction.SAVE,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                'Save',
                Gtk.ResponseType.OK,
            ),
        )

        self._window = window

    def export_photo(self, photo):
        # TODO: photo is actually an photoshell.image.Image

        response = self.run()

        if response == Gtk.ResponseType.OK:
            filename = self.get_filename()
        else:
            filename = None

        def write_image(photo, format, filename):
            # TODO: Export the full sized photo, not the preview.
            with Image(filename=photo.developed_path) as image:
                image.format = format
                image.save(filename=filename)

        if filename and response == Gtk.ResponseType.OK:
            extension = os.path.splitext(filename)[-1]
            if extension.lower() == '.png':
                write_image(photo, 'png', filename)
            elif extension.lower() in ['.jpg', '.jpeg']:
                write_image(photo, 'jpeg', filename)
            else:
                # TODO: show error here
                pass

        self.destroy()
