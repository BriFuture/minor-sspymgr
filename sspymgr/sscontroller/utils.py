# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from sspymgr.path_helper import createLogger
logger = createLogger('sscontroller', stream=False, logger_prefix="[Core SSController]")

import sys, os
def ssAddr(addr2str = False):
    """Get universe address for communicating with shadowsocks server
    """
    if sys.platform.startswith( 'linux' ):
        mgr_addr = '/var/run/sspymgr.sock'
    else:
        mgr_addr = ('127.0.0.1', 6001)

    # some problem in unix sock file, using tcp mode always
    mgr_addr = ('127.0.0.1', 6001)

    if addr2str:
        mgr_addr = '{}:{}'.format( mgr_addr[0], mgr_addr[1])
    return mgr_addr
    