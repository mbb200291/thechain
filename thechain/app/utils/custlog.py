import logging
import sys
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter


def get_formator():
    color_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s  %(name)-15s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    return color_formatter

def get_normal_formator():
    formatter = logging.Formatter(
        "%(asctime)s  %(name)-15s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return formatter


def setup_logger(name, log_file='app.log', level=logging.INFO):


    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(get_normal_formator())

    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
    file_handler.setFormatter(get_normal_formator())

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
