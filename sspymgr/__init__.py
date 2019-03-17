# -*- coding:utf-8 -*-
"""sspymgr: a website application for managing shadowsocks service 
"""

__author__ = 'BriFuture'
__version__ = '0.0.20'

from .manager import Manager
# models
from .models import DB

from .path_helper import createLogger, createLoggerFile
from .globalfuncs import isEmailMatched, getRandomCode, convertFlowToByte, formatTime