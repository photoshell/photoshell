import os

from gi.repository import Gtk, GdkPixbuf, Gio
from PIL import Image


def load_image(file_name):
    loader = GdkPixbuf.PixbufLoader.new()
    loader.write(open(file_name, 'rb').read())
    loader.close()

    # Get Image Data
    image = Image.open(file_name)
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

    for root, dirs, files in os.walk(os.path.join(library, 'thumbnail')):
        for file_name in files:
            if file_name.split('.')[-1] in ['jpg', 'JPG']:
                file_names.append(os.path.join(root, file_name))

    current_image = None
    current_file = 0

    def prev_image(button):
        nonlocal current_image
        nonlocal current_file
        window.remove(current_image)
        current_file = (current_file - 1) % len(file_names)
        current_image = load_image(file_names[current_file])
        window.add(current_image)
        window.show_all()

    def next_image(button):
        nonlocal current_image
        nonlocal current_file
        window.remove(current_image)
        current_file = (current_file + 1) % len(file_names)
        current_image = load_image(file_names[current_file])
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
    current_image = load_image(file_names[current_file])
    window.add(current_image)
    window.show_all()

    # Start the GTK loop
    Gtk.main()
