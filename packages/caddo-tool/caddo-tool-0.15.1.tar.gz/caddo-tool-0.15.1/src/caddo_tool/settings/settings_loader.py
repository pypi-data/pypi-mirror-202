import os
import sys

import yaml
from yaml import SafeLoader

from caddo_tool.settings.settings import Settings


class SettingsLoader:
    def __init__(self):
        self.settings_path = f'{os.getcwd()}/settings.yaml'
        if sys.argv[1] == '--configuration':
            self.settings_path = str(sys.argv[2])

    def load(self):
        print("LOADING SETTINGS:")
        self.load_settings_object()
        print()

    def read_settings_file(self):
        with open(self.settings_path) as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data

    def load_settings_object(self):
        settings_file = self.read_settings_file()
        print("Settings:")
        print(yaml.dump(settings_file, default_flow_style=False))
        Settings.input_data_file = settings_file['data']['path']
        Settings.model_initializer_module_path = settings_file['modules']['model_initializer']
        Settings.data_preprocessor_module_path = settings_file['modules']['data_preprocessor']
        Settings.model_trainer_module_path = settings_file['modules']['model_trainer']
        Settings.model_tester_module_path = settings_file['modules']['model_tester']
        Settings.model_evaluator_module_path = settings_file['modules']['model_evaluator']
        Settings.summarizer_module_path = settings_file['modules']['summarizer']
