from gi.repository import Gtk


class Slideshow(Gtk.Box):

    def __init__(self):
        super(Slideshow, self).__init__()
        self.empty_label = Gtk.Label()
        self.empty_label.set_text('Your library is empty.')
        self.set_image(self.empty_label)

    def render_selection(self, selection):
        self.remove(self.image)

        new_image = selection.current()
        if new_image:
            self.set_image(new_image.load_preview(selection.library_path))
        else:
            self.set_image(self.empty_label)

    def set_image(self, image):
        self.image = image
        self.pack_start(self.image, True, True, 0)
