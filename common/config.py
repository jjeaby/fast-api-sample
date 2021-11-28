import os
from configparser import ConfigParser
from os import environ

from common.Log import Log
from common.util import root_path


class Config(object):
    __config__ = None

    @staticmethod
    def dict():
        """
        Load Configuration information from config.ini file
        """
        config_parse = ConfigParser()
        config_file = os.path.join(root_path(), 'config', 'config.ini')
        config_parse.read(config_file)

        return config_parse[environ.get("RUN_MODE", "LOCAL")]

    def __init__(self):
        logger = Log.__logger__
        if Config.__config__:
            logger.info("Configure Instance cannot be instantiated more than once")
        else:
            self.dict()
            Config.__config__ = self.dict()


Config()
