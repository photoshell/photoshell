import os
import sys

import yaml

from photoshell import ui

config_path = os.path.join(os.environ['HOME'], '.photoshell.yaml')

config = dict(
    {
        'library': os.path.join(os.environ['HOME'], 'Pictures/Photoshell')
    }
)
if os.path.isfile(config_path):
    with open(config_path, 'r') as config_file:
        config = yaml.load(config_file)
else:
    with open(config_path, 'w+') as config_file:
        yaml.dump(config, config_file, default_flow_style=False)

print('Libray path is {0}'.format(config['library']))

# Open photo viewer
ui.render(config['library'])
