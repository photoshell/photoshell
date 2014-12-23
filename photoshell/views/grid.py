import threading

from gi.repository import Gtk


class Grid(Gtk.ScrolledWindow):

    def __init__(self):
        super(Grid, self).__init__()
        self.flowbox = Gtk.FlowBox()
        self.add(self.flowbox)

    def render_selection(self, selection):
        photos = []

        for image in selection.each():
            box = Gtk.Box()
            box.set_size_request(256, 256)
            self.flowbox.add(box)
            photos.append((image, box))

        def load_thumbnails():
            nonlocal selection

            for photo, box in photos:
                box.add(photo.load_preview(selection.library_path, 256, 256))
                self.show_all()

        thread = threading.Thread(target=load_thumbnails)
        thread.daemon = True
        thread.start()
