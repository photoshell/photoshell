import os

from gi.repository import GdkPixbuf
from gi.repository import Gtk
import wand.image


class Image(object):

    def __init__(self, image_path, datetime):
        self.image_path = image_path
        self.datetime = datetime

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

    def load_pixbuf(self, base_path, max_width=1280, max_height=1024):
        loader = GdkPixbuf.PixbufLoader.new()
        loader.write(open(self.image_path, 'rb').read())
        loader.close()

        # Get Image Data
        with wand.image.Image(filename=self.image_path) as image:
            width, height = image.size

        scale = min(max_height / height, min(max_width / width, 1))

        width = width * scale
        height = height * scale

        # Create Pixbuf
        pixbuf = loader.get_pixbuf().scale_simple(
            width, height, GdkPixbuf.InterpType.BILINEAR)
        pixbuf = pixbuf.scale_simple(
            width, height, GdkPixbuf.InterpType.BILINEAR)

        return pixbuf

    def load_preview(self, base_path, max_width=1280, max_height=1024):
        return Gtk.Image.new_from_pixbuf(self.load_pixbuf(base_path, max_width, max_height))
