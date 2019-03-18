# -*- coding: utf-8 -*-
"""Description: This module is used for integrating shadowsocks in sspymgr, it defines the configuration file
that shadowsocks server should read when it starts. It also provides a very convenient way to start shadowsocks
server in a seperated thread without effecting the webserver of sspymgr. If only the shadowsocks server should 
be launched, invoke the ``main`` functin with wait keyword to be True in case the main thread finishes and then
the single thread with shadowsocks server running within it ends up. Please note: the output of the shadowsocks
server is redirected to a LOG file whose name is 'shadowsocks.log', placed under Universal Log Dir For sspymgr.

Author: BriFuture

Date: 2019/03/19
"""
import sys, os

from sspymgr import tr
from sspymgr.path_helper import createLoggerFile, DATA_DIR
from sspymgr.sscontroller import ssAddr

_config_file = '/server-multi-passwd.json'
def ssConfigFile(filename = '/server-multi-passwd.json'):
    """Get the configuration file for shadowsocks server, 
    TODO  able to change the config file when command-line options specified
    """
    config = DATA_DIR + filename
    if( not os.path.exists( config ) ):
        
        DEFAULT_CONFIG = """{
    "server": "0.0.0.0",
    "server_port": 0,
    "timeout": 300,
    "method": "aes-256-cfb",
    "fast_open": false
}
"""
        with open( config, 'w', encoding="utf-8") as f:
            f.write( DEFAULT_CONFIG )
    return config


def _runSS():
    """Deprecated, the launch process of shadowsocks server needs some configuration on the arguments option 
    which would modify ``sys.argv``, so it may contain potential problem if the sspymgr is started with some
    options.

    At the very begging of this project when there is no logger and command-line argument options for sspymgr,
    this method works fine, but as the project gets completed, this simple way to start shadowsocks server is
    no longer satisfied with the demands. 
    """
    mgr_addr = ssAddr(True)
    args = '--manager-address %s -c %s' % ( mgr_addr, ssConfigFile() )
    sys.argv[1:] = args.split( ' ' )   
    from shadowsocks import server
    server.main()

def new_runSS():
    """An effective way to start shadowsocks server with all the outputs of it redirected into a log file
    named `shadowsocks.log` under `~/.sspy-mgr/logs`.
    """
    import logging
    fileHandler = createLoggerFile('shadowsocks')
    logger = logging.getLogger()
    logger.addHandler(fileHandler)
    logger.setLevel(logging.INFO)

    from shadowsocks import shell, daemon, eventloop, manager
    logger.info( 'Start running shadowsock server')
    shell.check_python()
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    config_path = ssConfigFile()
    logger.info(tr('Loading configuration from {}').format(config_path))
    with open(config_path, 'rb') as f:
        try:
            config = shell.parse_json_in_str(f.read().decode('utf8'))
        except ValueError as e:
            logger.error("found an error in config.json: {}".format(e.message))
            sys.exit(1)
    config['manager_address'] = ssAddr(True)
    config['port_password'] = {}
    config['server_port'] = 0
    config['verbose'] = 2
    config['method'] = 'aes-256-cfb'

    daemon.daemon_exec(config)

    config['port_password'] = {}
    # server_port = config['server_port']
    # if type(server_port) == list:
    #     for a_server_port in server_port:
    #         config['port_password'][a_server_port] = config['password']
    # else:
    #     config['port_password'][str(server_port)] = config['password']

    logger.info('entering manager mode')
    manager.run(config)

def main(wait=False):
    """Set wait to true, the main process will wait shadowsocks process finished,
    it might be useful when webserver does not start.
    """
    ## The reason why Popen is not used is that the python interpreter should be specified to start the 
    ## sockserver. On some machines which contains both python2.x and python3.x, and python is linked to
    ## python2, that may cause some conflicts, so it's better to run the shadowsocks server in the sub
    ## Process and if sspymgr is launched normally, the sub process should be launched too if no error occurs.
    # import sys
    # from subprocess import Popen
    # with open( 'logfile.txt', 'ab' ) as file:
        # p = Popen( ['python', '-m', 'sockserver' ], stdin=sys.stdin, stdout=sys.stdout, stderr=file  ) 
    
    from multiprocessing import Process
    p = Process( target = new_runSS )
    p.daemon = True
    p.start()
    if wait:
        p.join()
    from time import sleep
    sleep( 1 )

if __name__ == '__main__':
    new_runSS()
