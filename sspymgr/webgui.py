# -*- coding: utf-8 -*-

__author__ = 'BriFuture'

from gevent import monkey
monkey.patch_all ()

from .configuration import defaultConfig
from .path_helper import createLogger
logger = createLogger("sspymgr")
config = defaultConfig()

app = None
def run_forever():
    # from 
    if config.stream_log:
        import sspymgr.path_helper as ph
        ph.log_to_console = True
    run_shadowsocks()
    if config.webserver:
        run_webserver()
    else:
        logger.info("Webserver sspymgr webserver not start. Only shadowsocks will running")

def run_shadowsocks():

    if config.shadowsocks or not config.webserver:
        from .sscontroller import start_shadowsocks
        wait = not config.webserver
        start_shadowsocks(wait=wait)
    else:
        logger.info("shadowsocks won't start.")

from .manager import Manager


def run_webserver():
    global app
    app = Manager( __name__ )
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

