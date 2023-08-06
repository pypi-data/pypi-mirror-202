import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
import datetime


def create_logger(name, path, **config):
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        r_handler = RotatingFileHandler(path, maxBytes=1024 * 1024, backupCount=0)
        formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
        r_handler.setFormatter(formatter)

        log_level = config.get('log_level')
        if log_level is None:
            logger.setLevel(level=logging.INFO)
            r_handler.setLevel(level=logging.INFO)
        elif log_level.upper() == 'DEBUG':
            logger.setLevel(level=logging.DEBUG)
            r_handler.setLevel(level=logging.DEBUG)
        elif log_level.upper() == 'WARNING':
            logger.setLevel(level=logging.WARNING)
            r_handler.setLevel(level=logging.WARNING)
        else:
            logger.setLevel(level=logging.INFO)
            r_handler.setLevel(level=logging.INFO)
        logger.addHandler(r_handler)
    return logger

