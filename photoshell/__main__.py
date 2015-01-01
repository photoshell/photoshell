import os

from gi.repository import GObject

from photoshell.config import Config
from photoshell.library import Library
from photoshell.views.slideshow import Slideshow
from photoshell.views.window import Window

c = Config({
    'library': os.path.join(os.environ['HOME'], 'Pictures/Photoshell'),
    'dark_theme': True,
    'import_path': '%Y-%m-%d/{original_filename}'
})

# Open photo viewer
library = Library(c)
Window(c, library, Slideshow())
c.flush()
