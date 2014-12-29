from threading import Lock

from gi.repository import Gtk


class Slideshow(Gtk.Box):

    def __init__(self):
        super(Slideshow, self).__init__()
        self.image = Gtk.Image()
        self.image_path = None
        self.pack_start(self.image, True, True, 0)
        self.mutex = Lock()

    def render_selection(self, selection):
        self.mutex.acquire()

        new_image = selection.current()

        if new_image:
            # TODO: image path is bad criteria for redrawing if we re-develop
            if self.image_path != new_image.image_path:
                self.image.set_from_pixbuf(
                    new_image.load_pixbuf(selection.library_path),
                )
                self.image_path = new_image.image_path

        self.mutex.release()
