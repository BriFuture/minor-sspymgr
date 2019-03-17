# -*- coding: utf-8 -*-

"""Description: Basic integrated entry for starting webserver and shadowsocks server in a main looped thread, 
It's possible to start only webserver or shadowsocks server seperately. But it needs some additional config 
in configuration file or with command arguments. SSPYMGR is not featured yet although it can work, so it won't be
updated for some time until I get some spare time to reconstruct it. 

Author: BriFuture

Modified: 2019/03/10 19:17
"""

__author__ = 'BriFuture'

from gevent import monkey
monkey.patch_all ()

from .configuration import defaultConfig
from .path_helper import createLogger
from .globalfuncs import initGettext
tr = initGettext()
logger = createLogger("sspymgr")
config = defaultConfig()

app = None
def run_forever():
    """Basic integrated entry for starting webserver and shadowsocks server in a main looped thread
    """
    # from 
    if config.stream_log:
        import sspymgr.path_helper as ph
        ph.log_to_console = True
    run_shadowsocks(config)
    if config.webserver:
        run_webserver()
    else:
        logger.info("Webserver sspymgr webserver not start. Only shadowsocks will running")

def run_shadowsocks(config):
    """Start shadowsocks through api provided by sscontroller sub module.
    """
    if config.shadowsocks or not config.webserver:
        from .sscontroller import start_shadowsocks
        wait = not config.webserver
        start_shadowsocks(wait=wait)
    else:
        logger.info("shadowsocks won't start.")

from .manager import Manager


def run_webserver():
    """Start webserver application, the application is an instance of Mananger which is a subclass of Flask
    Currently it will only show debug info when running under debug mode, but it's a little annoying that the 
    templates won't be auto reloaded if the application is not running under debug mode.
    Or maybe it's more resanonable if this function is a method of Manager. But now it will keep unchanged.
    """
    global app
    app = Manager( __name__ )
    from .core import init as core_init
    core_init(app)
    app.start()

    from gevent import pywsgi
    weblogger = createLogger("webwsgi")

    if config.debug:
        from werkzeug.debug import DebuggedApplication
        app.debug = True
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        dapp = DebuggedApplication( app, evalex= True)
        server = pywsgi.WSGIServer( ( config.host, config.port ), 
            dapp, log = weblogger )
        logger.info( 'starting web server...')
        server.serve_forever()
    else:
        app.debug = False
        server = pywsgi.WSGIServer( ( config.host, config.port ), 
            app, log = weblogger )
        logger.info('starting web server...')
        server.serve_forever()

