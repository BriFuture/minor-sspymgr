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

        with open( CONFIG_PATH, 'r', encoding='utf-8' ) as f:
            config_obj = yaml.load( f )
            self.__parse_yaml(config_obj)
        ## 命令行参数会覆盖掉配置文件的设置
        self.__parse_sys_argv()
        self.__check_configuration()

    def __parse_yaml(self, yamlObj):
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
        self.webserver = config.get('webserver', True)

    def __parse_sys_argv(self):
        parser = argparse.ArgumentParser(description='Run SSPYMGR. Support Python3.x only.')

        parser.add_argument("--log_console", 
            help="Logger output will send to stdout.", action="store_true")

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

        args = parser.parse_args()
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