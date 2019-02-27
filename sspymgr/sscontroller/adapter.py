# -*- coding: utf-8 -*-
"""负责底层操作，如：与 shadowsock 服务器交互
"""

import socket 
# from gevent import socket, spawn, joinall
# from gevent.pool import Pool
import os, sys
DEFAULT_METHOD = "aes-256-cfb"
from .utils import logger
# from .database import db, Account, Command

class SSProtocol( object ):
    """only generate corresponding string, not communicate with shadowsocks server
    """
    def ping( self ):
        return b'ping', b'pong'

    def add_port( self, port, password, method ):
        cmd = 'add: {{ "server_port": {:d}, "password": "{:s}", "method": "{:s}" }}'.format( port, password, method)
        # command = Command(code=cmd)
        # db.session.add
        return cmd.encode( 'ascii' ), b'ok', True, port
    
    def remove_port( self, port ):
        cmd = "remove: {{ 'server_port': {:d} }}".format(port)
        return cmd.encode( 'ascii' ), b'ok', False, port

# import re
# STAT = re.compile( b'stat: {[^s]+}' )
import json
from queue import Queue
from time import sleep

class SSAdapter( object ):
    """contains two queues, one of which contains commands to be sent,
    one of which contains string recieved
    """

    def __init__( self, stater ):
        self.stater = stater
        self.queue = Queue()
        self.protocol = SSProtocol()
        self.accounts = dict() # key is port: int, value is another dict
        self.stat_count = 0

    def conn_ser( self, server ):
        if type( server ) is not tuple:
            from threading import current_thread
            name = current_thread().name
            sock_file = '/tmp/sspymgr_control_%s.sock'  % name  # if more than one thread using same file, problems will definately occure
            try:
                os.unlink( sock_file )
            except Exception as exc:
                # print( 'error: ', exc )
                pass

            self._socket = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
            self._socket.bind( sock_file )
        else:
            self._socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )  ## UDP connection

        # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.settimeout( 0 )  # timeout
        self._socket.setblocking( False ) # block
        self._socket.connect( server )
        self.ping()


    def ping( self ):
        cmd = self.protocol.ping()
        self.queue.put( cmd )

    def add_port( self, port: int, password: str, method=DEFAULT_METHOD ):
        """add processing status: created -> added
        """
        self.accounts[ port ] = { 'flow': 0, 'status': 'created' }

        cmd = self.protocol.add_port(port, password, method)
        logger.debug("port is adding : {}".format(cmd))
        self.queue.put( cmd )
    
    def remove_port( self, port: int ):
        if port not in self.accounts:
            return
        self.accounts[ port ] = { 'flow': 0, 'status': 'removing' }
        cmd = self.protocol.remove_port(port)
        logger.debug("port is removing : {}".format(cmd))
        self.queue.put( cmd )
    
    def update_port( self, port: int, password: str, method = DEFAULT_METHOD):
        self.remove_port( port )
        self.add_port( port, password, method )

    def contains_port( self, port: int ):
        return port in self.accounts

    def execute(self):
        cmd = None
        if not self.queue.empty():
            cmd = self.queue.get()
            # logger.debug("sending: {}".format(cmd))
            self._socket.send( cmd[0] )
            sleep(0.005)
        try:
            rmsg = self._socket.recv( 2048 )
            logger.debug("resp: {} cmd: {}".format(rmsg, cmd))
            self._processResponse(rmsg, cmd)
        except Exception as exc:
            if type(exc) != BlockingIOError:
                logger.warn("cmd executing error: {}".format(exc) )
            

        self.stat_count += 1

        if( self.stat_count == 60 ):
            """avoid long time not recved stats information
            """
            # self.ping()
            logger.debug("SSServer not response for a long time")
            self.stater( self.accounts, force=True )
            self.stat_count = 0

    def _processResponse(self, rmsg, cmd=None):
        """stats is a dict, contains port and flow.
        for example:
            { "45000", 1234, "45001": 5555 }
        """
        if cmd is None and rmsg[:4] == b'stat':
            stats = rmsg[ 5: ]
            stats = json.loads( stats )
            for key in stats:
                self.accounts[ int( key ) ]['flow'] += stats[ key ]
            self.stater( self.accounts )
            self.stat_count = 0
            return

        # logger.debug( 'recv: {}, cmd: {}'.format(rmsg, cmd) )
        if rmsg != cmd[1]:
            return
        if len(cmd) < 3:
            logger.info( 'Recved Pong from server' )
            self.stat_count = 0
            return

        add = cmd[ 2 ]
        port = cmd[ 3 ]
        logger.info( 'port {} is added: {}'.format(port, add) )
        if add:
            self.accounts[ port ]['status'] = 'added'
        else:
            self.accounts[ port ]['status'] = 'removed'
            # self.accounts[ port ]['flow'] = 0
        # logger.debug( self.accounts )

        
