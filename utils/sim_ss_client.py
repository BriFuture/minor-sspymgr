# -*- coding: utf-8 -*-

# from socket import socket, AF_INET, SOCK_DGRAM
from gevent import socket, spawn, joinall

class SSProtocol( object ):
    """only generate corresponding string, not communicate with shadowsocks server
    """
    def ping( self ):
        return b'ping', b'pong'

    def add_port( self, port, password ):
        cmd = 'add: { "server_port": %d, "password": "%s", "method": "aes-256-cfb" }' % ( port, password )
        return cmd.encode( 'ascii' ), b'ok'
    
    def remove_port( self, port ):
        cmd = 'remove: { "server_port": %d }' % port
        return cmd.encode( 'ascii' ), b'ok'


from time import sleep
def main():
    while True:
        send()
        sleep( 0.5 )

pro = SSProtocol()
send_sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
send_sock.connect( ('localhost', 6001 ) )
# send_sock.setblocking( False )
added = False
count = 0
def send():
    global send_sock, pro, added, count
    send_sock.send( pro.ping()[0] )
    print( 'ping', count, send_sock.recv( 1024 ) )
    count += 1
    if not added:
        send_sock.send( pro.add_port( 80, '123456' )[0] )
        print( 'send', send_sock.recv( 1024 ) )
        added = True

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        send_sock.shutdown(socket.SHUT_RDWR)
        send_sock.close()
        print( 'closed' )

