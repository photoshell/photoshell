import os

from gi.repository import Gtk, GdkPixbuf, Gio
from wand.image import Image

from photoshell.library import Library


def load_image(file_name):
    loader = GdkPixbuf.PixbufLoader.new()
    loader.write(open(file_name, 'rb').read())
    loader.close()

    # Get Image Data
    with Image(filename=file_name) as image:
        width, height = image.size

    # TODO: Don't hard code this
    max_height = 1024
    max_width = 1280

    scale = min(max_height / height, min(max_width / width, 1))

    width = width * scale
    height = height * scale

    # Create Pixbuf
    pixbuf = loader.get_pixbuf().scale_simple(
        width, height, GdkPixbuf.InterpType.BILINEAR)
    pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

    return Gtk.Image.new_from_pixbuf(pixbuf)


def render(library):
    # Use Dark Theme
    settings = Gtk.Settings.get_default()
    settings.set_property('gtk-application-prefer-dark-theme', True)

    # Load Images
    file_names = []

    selection = Library(library).all()

    current_image = None

    def prev_image(button):
        set_image(selection.next().thumbnail)

    def next_image(button):
        set_image(selection.prev().thumbnail)

    def set_image(image_name):
        nonlocal current_image
        window.remove(current_image)
        current_image = load_image(image_name)
        window.add(current_image)
        window.show_all()

    # Create Header
    header_bar = Gtk.HeaderBar()
    header_bar.set_show_close_button(True)
    header_bar.props.title = 'PhotoShell'

    navigation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    Gtk.StyleContext.add_class(navigation_box.get_style_context(), 'linked')

    prev_button = Gtk.Button()
    prev_button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
    prev_button.connect('clicked', prev_image)
    navigation_box.add(prev_button)

    next_button = Gtk.Button()
    next_button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
    next_button.connect('clicked', next_image)
    navigation_box.add(next_button)

    import_button = Gtk.Button()
    import_icon = Gio.ThemedIcon(name="insert-image-symbolic")
    import_image = Gtk.Image.new_from_gicon(import_icon, Gtk.IconSize.BUTTON)
    import_button.add(import_image)

    settings_button = Gtk.Button()
    settings_icon = Gio.ThemedIcon(name="emblem-system-symbolic")
    settings_image = Gtk.Image.new_from_gicon(
        settings_icon, Gtk.IconSize.BUTTON)
    settings_button.add(settings_image)
    header_bar.pack_end(settings_button)

    terminal_button = Gtk.Button()
    terminal_icon = Gio.ThemedIcon(name="utilities-terminal-symbolic")
    terminal_image = Gtk.Image.new_from_gicon(
        terminal_icon, Gtk.IconSize.BUTTON)
    terminal_button.add(terminal_image)
    header_bar.pack_end(terminal_button)

    header_bar.pack_start(navigation_box)
    header_bar.pack_start(import_button)

    # Setup Window
    window = Gtk.Window()
    window.set_titlebar(header_bar)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect('delete-event', Gtk.main_quit)
    current_image = load_image(selection.current().thumbnail)
    window.add(current_image)
    window.show_all()

    # Start the GTK loop
    Gtk.main()
