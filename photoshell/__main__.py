import os
import signal

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

signal.signal(signal.SIGINT, signal.SIG_DFL)
Window(c, library, Slideshow())

if c.exists():
    c.flush()
