from threading import Lock

from gi.repository import Gtk


class Slideshow(Gtk.Box):

    def __init__(self):
        super(Slideshow, self).__init__()
        self.image = Gtk.Image()
        self.photo_hash = None
        self.pack_start(self.image, True, True, 0)
        self.mutex = Lock()

    def render_selection(self, selection):
        self.mutex.acquire()

        new_image = selection.current()

        if new_image:
            if self.photo_hash != new_image.hash_code:
                self.image.set_from_pixbuf(
                    new_image.load_pixbuf(selection.library_path),
                )
                self.photo_hash = new_image.hash_code,

        self.mutex.release()
