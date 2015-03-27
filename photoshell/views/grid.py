import threading

from gi.repository import Gtk
from gi.repository import GLib

from photoshell.gtk.image_cache import GtkImageCache


THUMB_WIDTH = 256
THUMB_HEIGHT = 256


class PhotoBox(Gtk.Box):

    def __init__(self, photo):
        super(PhotoBox, self).__init__()
        self.photo = photo


class Grid(Gtk.ScrolledWindow):

    def __init__(self):
        super(Grid, self).__init__()
        self.image_cache = GtkImageCache()
        self.flowbox = Gtk.FlowBox()
        self.add(self.flowbox)

    def render_selection(self, selection):
        # TODO: actually handle updates
        self.get_children()[0].remove(self.flowbox)
        self.flowbox = Gtk.FlowBox()
        self.get_children()[0].add(self.flowbox)

        photo_boxes = []

        for photo in selection.each_photo():
            box = PhotoBox(photo)
            box.set_size_request(THUMB_WIDTH, THUMB_HEIGHT)
            self.flowbox.add(box)
            photo_boxes.append(box)

        self.show_all()

        def load_thumbnails():
            for photo_box in photo_boxes:
                gtk_image = self.image_cache.gtk_image(
                    selection.library_path,
                    photo_box.photo,
                    THUMB_WIDTH,
                    THUMB_HEIGHT,
                )
                GLib.idle_add(photo_box.set_center_widget, gtk_image)
                GLib.idle_add(photo_box.show_all)

        load_thread = threading.Thread(target=load_thumbnails)
        load_thread.daemon = True
        load_thread.start()
