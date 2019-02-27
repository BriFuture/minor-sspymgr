# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath( os.path.dirname( __file__) )
import yaml
from pathlib import Path
from .path_helper import CONFIG_PATH
import argparse

class Configuration:
    SECRET_KEY = os.environ.get( 'SECRET_KEY' ) or 'ITISAHARDGUESSSTRING'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    
    def __init__(self, *args, **kwargs):
        self.parse()
        pass
    
    def parse( self ):
        if not os.path.exists( CONFIG_PATH ):
            _write_default_config()

        ## part of arguments from command line will cover the configuration from config.file
        self.__parse_sys_argv()
        self.__check_configuration()

    def __parse_yaml(self, path: Path):
        with path.open( 'r', encoding='utf-8' ) as f:
            yamlObj = yaml.load( f )
            self.raw_config = yamlObj
            mgrconfig = yamlObj['sspymgr']
            self.email = yamlObj['email']
            self.debug = False
            if 'debugConfig' in mgrconfig:
                if mgrconfig['debugConfig']['enabled']:
                    config = mgrconfig['debugConfig']
                    self.debug = True
                else:
                    config = mgrconfig['config']
            else:
                config = mgrconfig['config']
            self.host = config['host']
            self.port = config['port']
            self.shadowsocks = config.get('shadowsocks', True)
            self.webserver   = config.get('webserver', True)

    def __parse_sys_argv(self):
        parser = argparse.ArgumentParser(description='Run SSPYMGR. Support Python3.x only.')

        self.__add_arguments(parser)

        args = parser.parse_args()
        
        self.database = "database"

        if args.config is not None:
            index = args.config.find(".yaml")
            try:
                p = Path(args.config)
                if index > -1:
                    self.database = args.config[:index]
                self.__parse_yaml(p)
            except:
                p = Path(CONFIG_PATH)
                self.__parse_yaml(p)
        else:
            p = Path(CONFIG_PATH)
            self.__parse_yaml(p)

            
        if args.webhost is not None:
            self.host = args.webhost
        if args.disable_ss:
            self.shadowsocks = False
        if args.only_ss:
            self.shadowsocks = True
            self.webserver = False


        self.stream_log = args.log_console
        # -w start web gui server
        # -s start shadowsocks server

    def __add_arguments(self, parser):
        parser.add_argument("--log_console", 
            help="Logger output will send to stdout.", action="store_true")
        parser.add_argument("-c", "--config", 
            help="Specify configuration file (absolute path), sspymgr will create a new database file whose name is the same as the configuration file, \
                for example, -c ~/.sspy-mgr/local.yaml will create a database named ~/.sspy-mgr/local.db", nargs="?")

        webgroup = parser.add_argument_group('website', 'website options')
        webgroup.add_argument("--webhost", help="Set IP address that web werver listens, \
            for example 0.0.0.0 for IPv4, :: for IPv6", nargs="?")
        webgroup.add_argument("--webport", help="Set port that Website listens, usually 80", nargs="?")

        ssgroup = parser.add_argument_group('shadowsocks', 'integrated shadowsocks opration')
        ssgroup.add_argument("--disable_ss", help="Enable backend shadowsocks server,\
            disable it when developing the program may be helpful", 
            action="store_true")
        ssgroup.add_argument("--only_ss", help="Only start backend shadowsocks server \
            with defined communication method (socket or unix sock file) ", 
            action="store_true")

    def __check_configuration(self):
        ## TODO check host valid

        pass

def _write_default_config( self ):
    """only call this method when needed, or config file may be overrided
    """
    with open( CONFIG_PATH, 'w', encoding='utf-8' ) as f:
        default = """email:
  account: 'your@account.xx'
  password: 'your password'
  host: 'smtp host'
sspymgr:
  debugConfig: 
    enabled: false # true to override following config
    host: '127.0.0.1'
    port: 5050
    shadowsocks: false
  config:
    host: '0.0.0.0'
    port: 80
    shadowsocks: true
"""
        f.write( default )

__config = None
def defaultConfig() -> Configuration:
    """get single instance of the configuration 
    """
    global __config
    if __config is None:
        __config = Configuration()
    
    return __config