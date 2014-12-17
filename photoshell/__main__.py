import os

import yaml


config_path = os.path.join(os.environ['HOME'], '.photoshell.yaml')

with open(config_path, 'r') as config_file:
    config = yaml.load(config_file)

print('Libray path is {0}'.format(config['library']))
