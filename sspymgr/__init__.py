# -*- coding:utf-8 -*-
"""
    sspymgr
    website application for managing shadowsocks service 
"""

__author__ = 'BriFuture'
__version__ = '0.0.16'

# models
from .models import db

from .path_helper import createLogger, createLoggerFile
from .globalfuncs import getRandomCode, convertFlowToByte, formatTime