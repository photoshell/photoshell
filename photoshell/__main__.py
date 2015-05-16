import os
import signal

from enum import Enum

from photoshell.config import Config
from photoshell.library import Library
from photoshell.views.slideshow import Slideshow
from photoshell.views.window import Window


class UI(Enum):
    cli = 0
    gui = 1


def setup(ui=UI.cli):
    """
    Setup the main photoshell app.

    Parameters:
      ui (UI enum) — Use the GUI or the CLI
    """
    c = Config({
        'library': os.path.join(os.environ['HOME'], 'Pictures/Photoshell'),
        'dark_theme': True,
        'import_path': '%Y-%m-%d/{original_filename}'
    })

    # Open photo viewer
    library = Library(c)
    window = None
    if ui == UI.gui:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        window = Window(c, library, Slideshow())

        if c.exists():
            c.flush()

    return (c, library, window)

if __name__ == "__main__":
    from gi.repository import Gtk
    setup(ui=UI.gui)
    Gtk.main()
