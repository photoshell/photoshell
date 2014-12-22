from gi.repository import Gio
from gi.repository import Gtk

from photoshell.views.photo_import import PhotoImporter


class Window(Gtk.Window):

    def __init__(self, library, primary_view):
        super(Window, self).__init__()

        self.library = library
        self.primary_view = primary_view
        self.selection = library.all()

        # Use Dark Theme
        settings = Gtk.Settings.get_default()
        settings.set_property('gtk-application-prefer-dark-theme', True)

        # Create Header
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = 'PhotoShell'

        # Create navigation box
        navigation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(
            navigation_box.get_style_context(), 'linked')

        prev_button = Gtk.Button()
        prev_button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        prev_button.connect('clicked', self.prev_photo)
        navigation_box.add(prev_button)

        next_button = Gtk.Button()
        next_button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        next_button.connect('clicked', self.next_photo)
        navigation_box.add(next_button)

        self.header_bar.pack_start(navigation_box)

        # Create import button
        self.import_button = Gtk.Button()
        import_icon = Gio.ThemedIcon(name="insert-image-symbolic")
        import_image = Gtk.Image.new_from_gicon(
            import_icon, Gtk.IconSize.BUTTON)
        self.import_button.connect('clicked', self.import_folder)
        self.import_button.add(import_image)

        self.header_bar.pack_start(self.import_button)

        self.progress = Gtk.ProgressBar()
        self.progress.set_text('Importing...')
        self.progress.set_show_text(True)

        # Create settings button
        settings_button = Gtk.Button()
        settings_icon = Gio.ThemedIcon(name="emblem-system-symbolic")
        settings_image = Gtk.Image.new_from_gicon(
            settings_icon, Gtk.IconSize.BUTTON)
        settings_button.add(settings_image)
        self.header_bar.pack_end(settings_button)

        # Create terminal button
        terminal_button = Gtk.Button()
        terminal_icon = Gio.ThemedIcon(name="utilities-terminal-symbolic")
        terminal_image = Gtk.Image.new_from_gicon(
            terminal_icon, Gtk.IconSize.BUTTON)
        terminal_button.add(terminal_image)
        self.header_bar.pack_end(terminal_button)

        # Setup Window
        self.set_titlebar(self.header_bar)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('delete-event', Gtk.main_quit)
        self.set_default_size(800, 600)
        self.add(primary_view)
        self.primary_view.render_selection(self.selection)
        self.show_all()

        # Start the GTK loop
        Gtk.main()

    def render_selection(self, selection):
        self.selection = selection
        self.primary_view.render_selection(selection)
        self.show_all()

    def next_photo(self, button):
        self.selection.next()
        self.render_selection(self.selection)

    def prev_photo(self, button):
        self.selection.prev()
        self.render_selection(self.selection)

    def import_folder(self, button):
        PhotoImporter(self).import_photos()
