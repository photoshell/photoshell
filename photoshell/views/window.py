from gi.repository import Gio
from gi.repository import Gtk

from photoshell.views.grid import Grid
from photoshell.views.photo_import import PhotoImporter
from photoshell.views.slideshow import Slideshow


class Window(Gtk.Window):

    def __init__(self, config, library, primary_view):
        super(Window, self).__init__()

        self.library = library
        self.primary_view = None
        self.selection = library.all()

        # Use Dark Theme
        settings = Gtk.Settings.get_default()
        if 'dark_theme' in config and config['dark_theme'] == True:
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

        # Create view box
        view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(
            view_box.get_style_context(), 'linked')

        slideshow_button = Gtk.RadioButton()
        slideshow_button.set_property('draw-indicator', False)
        slideshow_icon = Gio.ThemedIcon(name="view-paged-symbolic")
        slideshow_image = Gtk.Image.new_from_gicon(
            slideshow_icon, Gtk.IconSize.BUTTON)
        slideshow_button.add(slideshow_image)
        view_box.add(slideshow_button)
        slideshow_button.connect('clicked', self.slideshow_view)

        grid_button = Gtk.RadioButton.new_from_widget(slideshow_button)
        grid_button.set_property('draw-indicator', False)
        grid_icon = Gio.ThemedIcon(name="view-grid-symbolic")
        grid_image = Gtk.Image.new_from_gicon(
            grid_icon, Gtk.IconSize.BUTTON)
        grid_button.add(grid_image)
        grid_button.connect('clicked', self.grid_view)

        view_box.add(grid_button)

        self.header_bar.pack_end(view_box)

        # Setup Window
        self.set_titlebar(self.header_bar)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('delete-event', Gtk.main_quit)
        self.set_default_size(800, 600)
        self.set_primary_view(primary_view)

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

    def slideshow_view(self, button):
        if type(self.primary_view) == Slideshow:
            return

        self.set_primary_view(Slideshow())

    def grid_view(self, button):
        if type(self.primary_view) == Grid:
            return

        self.set_primary_view(Grid())

    def set_primary_view(self, view):
        if self.primary_view:
            self.remove(self.primary_view)
        self.primary_view = view

        self.add(self.primary_view)
        self.primary_view.render_selection(self.selection)
        self.show_all()

    def import_folder(self, button):
        PhotoImporter(self).import_photos()
