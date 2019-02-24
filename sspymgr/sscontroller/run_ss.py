import sys, os

from sspymgr.path_helper import createLoggerFile, DATA_DIR
from sspymgr.sscontroller import ssAddr

def ssConfigFile():
    config = DATA_DIR + '/server-multi-passwd.json'
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


def runSS():
    mgr_addr = ssAddr(True)
    args = '--manager-address %s -c %s' % ( mgr_addr, ssConfigFile() )
    print(sys.argv)
    sys.argv[1:] = args.split( ' ' )   
    # import logging
    # logging.basicConfig(level=logging.INFO,
    #     format='%(asctime)s %(levelname)-8s %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S')
    from shadowsocks import server
    server.main()

def new_runSS():
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
    logger.info('loading config from %s' % config_path)
    with open(config_path, 'rb') as f:
        try:
            config = shell.parse_json_in_str(f.read().decode('utf8'))
        except ValueError as e:
            logger.error('found an error in config.json: %s',
                            e.message)
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
    # import logging
    # log = logging.getLogger( 'Test' )
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
    startSS()
