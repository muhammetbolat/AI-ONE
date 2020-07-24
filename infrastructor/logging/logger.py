import logging as log
import os

from models.configs.OtherConfig import OtherConfig


class Logger:
    def __init__(self, other_config: OtherConfig):
        self.other_config = other_config
        self.log_file = other_config.log_path
        self.log_level = log.DEBUG
        self.log_init()
        self.log = log

    def log_init(self):
        """
        initialization of log file.
        """
        log.basicConfig(filename=os.path.join(self.other_config.root_directory, self.log_file),
                        filemode='a',
                        format='%(asctime)s [%(levelname)s] - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=self.log_level)
