from threading import Lock

from gi.repository import Gtk


class Slideshow(Gtk.Box):

    def __init__(self):
        super(Slideshow, self).__init__()
        self.empty_label = Gtk.Label()
        self.empty_label.set_text('Your library is empty.')
        self.set_image(self.empty_label, None)
        self.mutex = Lock()

    def render_selection(self, selection):
        self.mutex.acquire()
        new_image = selection.current()

        if new_image:
            if self.photo_hash != new_image.hash_code:
                self.remove(self.image)

                self.set_image(
                    new_image.load_preview(selection.library_path),
                    new_image.hash_code,
                )
        else:
            self.remove(self.image)
            self.set_image(self.empty_label, None)

        self.mutex.release()

    def set_image(self, image, photo_hash):
        self.image = image
        self.photo_hash = photo_hash
        self.pack_start(self.image, True, True, 0)
