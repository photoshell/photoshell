import threading

from gi.repository import Gtk
from gi.repository import GLib


THUMB_WIDTH = 256
THUMB_HEIGHT = 256


class Grid(Gtk.ScrolledWindow):

    def __init__(self):
        super(Grid, self).__init__()
        self.flowbox = Gtk.FlowBox()
        self.add(self.flowbox)

    def render_selection(self, selection):
        # TODO: actually handle updates
        self.get_children()[0].remove(self.flowbox)
        self.flowbox = Gtk.FlowBox()
        self.get_children()[0].add(self.flowbox)

        photos = []

        for image in selection.each():
            box = Gtk.Box()
            box.set_size_request(THUMB_WIDTH, THUMB_HEIGHT)
            self.flowbox.add(box)
            photos.append((image, box))

        self.show_all()

        def load_thumbnails():
            for photo, box in photos:
                GLib.idle_add(box.set_center_widget, photo.load_preview(
                    selection.library_path, THUMB_HEIGHT, THUMB_HEIGHT))
                GLib.idle_add(box.show_all)

        load_thread = threading.Thread(target=load_thumbnails)
        load_thread.daemon = True
        load_thread.start()
