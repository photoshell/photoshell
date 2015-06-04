import os

from collections import UserDict

import yaml


class Config(UserDict):

    def __init__(self,
                 initialdata={},
                 path=os.path.join(os.environ.get('HOME', '.'), '.photoshell.yaml')):
        super(Config, self).__init__(initialdata)

        self.path = path
        self.load()

    def load(self):
        if os.path.isfile(self.path):
            with open(self.path, 'r') as config_file:
                try:
                    self.update(yaml.load(config_file))
                except:
                    pass

    def flush(self):
        with open(self.path, 'w+') as config_file:
            yaml.dump(self.data, config_file, default_flow_style=False)

    def exists(self):
        return os.path.exists(self.path)
