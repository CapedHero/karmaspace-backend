import logging.config

from logging_config import DICT_CONFIG


LOGGING_CONFIG = None
logging.config.dictConfig(DICT_CONFIG)
