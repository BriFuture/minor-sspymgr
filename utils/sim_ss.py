# -*- coding: utf-8 -*-

"""used for simulate shadowsocks server
"""

import sys
import json
OFFSET = 45000

from random import randint
def gen_stats( client: int ):
    stat = {}
    for i in range( 0, client ):
        port = OFFSET + i
        flow = randint( 3000, 500000 )
        stat[ str( port ) ] = flow
    return stat

from time import sleep
# from gevent import socket
from socketserver import BaseRequestHandler
# from socketserver import TCPServer
from socketserver import ThreadingUDPServer
from datetime import datetime
class StatsHandler( BaseRequestHandler ):
    def handle( self ):
        # print( 'Got connection from: ', self.client_address )
        while True:
            cmd, sock = self.request
            if not sock:
                break
            if cmd == b'ping':
                sock.sendto( b'pong', self.client_address )
            elif cmd.startswith( b'add' ):
                # cmd = cmd[4:]
                # cmdStr = json.loads( cmd )
                sock.sendto( b'ok', self.client_address )
            sleep( 1 )
            stats = gen_stats( 1 )
            statsStr = json.dumps( stats )
            msg = 'stat: ' + statsStr
            print( datetime.now(), msg )
            sock.sendto( msg.encode( encoding='ascii'), self.client_address )
            sleep( 120 )

def main():
    host = '127.0.0.1'
    port = 6001
    try:
        server = ThreadingUDPServer( ( host, port ), StatsHandler )
        server.serve_forever()
    except KeyboardInterrupt:
        print( 'Interrupted...')

if __name__ == '__main__':
    main()
