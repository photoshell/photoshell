from gi.repository import Gtk, GdkPixbuf
from PIL import Image


def render(file_name):
    # Use Dark Theme
    settings = Gtk.Settings.get_default()
    settings.set_property('gtk-application-prefer-dark-theme', True)

    # Load Image
    loader = GdkPixbuf.PixbufLoader.new()
    loader.write(open(file_name, 'rb').read())
    loader.close()

    # Get Image Data
    image = Image.open(file_name)
    width, height = image.size

    # Create Pixbuf
    pixbuf = loader.get_pixbuf().scale_simple(
        width, height, GdkPixbuf.InterpType.BILINEAR)

    # Setup Window
    window = Gtk.Window()
    window.set_title('Photo Viewer')
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect('delete-event', Gtk.main_quit)
    window.add(Gtk.Image.new_from_pixbuf(pixbuf))
    window.show_all()

    # Start the GTK loop
    Gtk.main()
