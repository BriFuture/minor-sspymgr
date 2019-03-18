# -*- coding: utf-8 -*-
"""Description: More convenient way for accessing specified path or file locaiton.
It's written a bit earlier as this project builds. I only know ``os.path`` to get
all path at that time, but as I learned more knowledge of python, I think it will
be better if they are replaced with pathlib.Path and it will be more readable. 

TODO rewrite/simplify this module, use pathlib instead of os.path for better readability.

Author: BriFuture

Modified: 2019/03/10 19:57
"""
import os, sys

from os.path import dirname, abspath, pardir, expanduser, join, exists

CURRENT_PATH = dirname(abspath(__file__))
TOP_PATH = abspath(join(CURRENT_PATH, os.pardir))  # ./../
USER_HOME = expanduser("~")

DATA_DIR = abspath(join(USER_HOME, '.sspy-mgr'))
LOG_DIR = abspath(join(DATA_DIR, 'log'))

#配置文件的绝对路径 absolute path
CONFIG_PATH = abspath(join(DATA_DIR, 'config.yaml'))

if not exists(DATA_DIR):
    os.mkdir(DATA_DIR)
if not exists(LOG_DIR):
    os.mkdir(LOG_DIR)

import logging


def createLoggerFile(name, level=logging.DEBUG) -> logging.FileHandler:
    """Create log file under specified directory
    """
    fmt = "%(asctime)s %(levelname)s:  %(message)s"
    formatter = logging.Formatter(fmt)
    if len(name) == 0:
        name = 'root'
    fp = abspath(join(LOG_DIR, '{}.log'.format(name)))
    fh = logging.FileHandler(fp)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    return fh

log_to_console = False
def createLogger(name, level=logging.DEBUG, stream=False, logger_prefix=""):
    """create logger for different modules
    @param ``name``: logger name. New Handlers won't be attached to the logger
    if logger already has Other Handlers.
    @param ``level`` set the lever of FileHandler, logging.DEBUG by default
    @param ``stream`` flag to indicate whether to add a StreamHandler, False by default
    """
    fh = createLoggerFile(name, level=level)

    logger = logging.getLogger(name)
    if len(logger.handlers) > 0:
        return logger
    logger.addHandler(fh)
    logger.setLevel(level)

    global log_to_console
    if stream or log_to_console:
        fmt = "%(asctime)s %(levelname)s: {} %(message)s".format(logger_prefix)
        formatter = logging.Formatter(fmt)
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    return logger
