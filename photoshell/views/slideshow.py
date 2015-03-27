from threading import Lock

from gi.repository import Gtk

from photoshell.gtk.image_cache import GtkImageCache


class Slideshow(Gtk.Box):

    def __init__(self):
        super(Slideshow, self).__init__()
        self.image_cache = GtkImageCache()
        self.image = Gtk.Image()
        self.image_path = None
        self.pack_start(self.image, True, True, 0)
        self.mutex = Lock()

    def render_selection(self, selection):
        self.mutex.acquire()

        new_photo = selection.current_photo()

        if new_photo:
            # TODO: image path is bad criteria for redrawing if we re-develop
            if self.image_path != new_photo.raw_path:
                self.remove(self.image)
                self.image = self.image_cache.gtk_image(
                    selection.library_path,
                    new_photo,
                )
                self.pack_start(self.image, True, True, 0)
                self.image_path = new_photo.raw_path

        self.mutex.release()
