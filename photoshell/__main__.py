import os
import sys

import yaml

from photoshell import ui


config_path = os.path.join(os.environ['HOME'], '.photoshell.yaml')

with open(config_path, 'r') as config_file:
    config = yaml.load(config_file)

print('Libray path is {0}'.format(config['library']))

# Open photo viewer
if len(sys.argv) > 1:
    ui.render(sys.argv[1])
