# -*- coding: utf-8 -*-
"""
project is under /home/future/minor-sspy-mgr which the TOP_PATH is,
本文件不依赖 sspymgr 中的其他项目
"""
import os, sys

from os.path import dirname, abspath, pardir, expanduser, join, exists

CURRENT_PATH = dirname(abspath(__file__))
TOP_PATH = abspath(join(CURRENT_PATH, os.pardir))  # ./../
USER_HOME = expanduser("~")

DATA_DIR = abspath(join(USER_HOME, '.sspy-mgr'))
LOG_DIR = abspath(join(DATA_DIR, 'log'))
"""配置文件的绝对路径
"""
CONFIG_PATH = abspath(join(DATA_DIR, 'config.yaml'))

if not exists(DATA_DIR):
    os.mkdir(DATA_DIR)
if not exists(LOG_DIR):
    os.mkdir(LOG_DIR)

import logging


def createLoggerFile(name, level=logging.DEBUG):
    """在统一的日志目录下创建日志文件，返回 FileHandler
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
    @param name logger name，若 logger 中已经包含 Handler，则不会添加新的 Handler
    level 设置新创建的 logger 的记录 level，默认为 DEBUG
    stream 是否设置流失处理器，默认为 False
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
