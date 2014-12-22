import os

from gi.repository import GdkPixbuf
from gi.repository import Gtk
import wand.image


class Image(object):

    def __init__(self, hash_code):
        self.hash_code = hash_code

        self._width = None
        self._height = None

    def width(self):
        if not self._width:
            pass

        return self._width

    def height(self):
        if not self._height:
            pass

        return self._height

    def load_preview(self, base_path):
        filename = os.path.join(
            base_path, 'thumbnail', '{0}.jpg'.format(self.hash_code))

        loader = GdkPixbuf.PixbufLoader.new()
        loader.write(open(filename, 'rb').read())
        loader.close()

        # Get Image Data
        with wand.image.Image(filename=filename) as image:
            width, height = image.size

        # TODO: Don't hard code this
        max_height = 1024
        max_width = 1280

        scale = min(max_height / height, min(max_width / width, 1))

        width = width * scale
        height = height * scale

        # Create Pixbuf
        pixbuf = loader.get_pixbuf().scale_simple(
            width, height, GdkPixbuf.InterpType.BILINEAR)
        pixbuf = pixbuf.scale_simple(
            width, height, GdkPixbuf.InterpType.BILINEAR)

        return Gtk.Image.new_from_pixbuf(pixbuf)
