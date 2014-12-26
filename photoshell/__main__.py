import os

from gi.repository import GObject
import yaml

from photoshell.library import Library
from photoshell.views.slideshow import Slideshow
from photoshell.views.window import Window

config_path = os.path.join(os.environ['HOME'], '.photoshell.yaml')

config = dict(
    {
        'library': os.path.join(os.environ['HOME'], 'Pictures/Photoshell'),
        'dark_theme': True
    }
)
if os.path.isfile(config_path):
    with open(config_path, 'r') as config_file:
        config = yaml.load(config_file)
else:
    with open(config_path, 'w+') as config_file:
        yaml.dump(config, config_file, default_flow_style=False)

# Open photo viewer
library = Library(config)
Window(config, library, Slideshow())
