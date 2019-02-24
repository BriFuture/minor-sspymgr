# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from sspymgr.path_helper import createLogger
logger = createLogger('sscontroller', stream=False, logger_prefix="[Core SSController]")

import sys, os
def ssAddr(addr2str = False):
    """获取统一的 SS 通信交互地址
    """
    if sys.platform == 'win32':
        mgr_addr = ('127.0.0.1', 6001)
    elif sys.platform.startswith( 'linux' ):
        mgr_addr = '/var/run/shadowsocks-manager.sock'
        try:
            os.unlink( mgr_addr )
        except Exception:
            pass

    # some problem in unix sock file, using tcp mode always
    mgr_addr = ('127.0.0.1', 6001)
    if addr2str:
        mgr_addr = '{}:{}'.format( mgr_addr[0], mgr_addr[1])
    return mgr_addr
    