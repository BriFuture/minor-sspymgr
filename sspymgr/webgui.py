# -*- coding: utf-8 -*-

__author__ = 'BriFuture'

from gevent import monkey
monkey.patch_all ()

from sspymgr.globalvars import config, events, tasker, \
    logger, controller, emailManager

def init_routes(app):
    # from .routes.vuefront import vuefront
    from .models import db

    @app.teardown_request
    def teardownd_database(resp):
        db.session.close()
        return resp

    from .routes import api
    # 用于添加其他的路由
    app.m_events.trigger('beforeRegisterApi', eventArgs = api )
    from .mail import registerApi as initEmail
    initEmail(api)
    app.register_blueprint( api, url_prefix='/api')

import threading
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def on_taskSchedule(schedule):
    controller.start()
    schedule.every().seconds.do(run_threaded, emailManager.checkRemain)


from flask import Flask

def init_all():
    """initialize all variables and databases.
    return Flask instance app.
    """
    app = Flask( __name__ )
    from .dbsessions import replaceSessionInterface
    replaceSessionInterface(app)

    app.m_events = events
    app.logger = logger
    app.m_emailManager = emailManager
    app.m_sscontroller = controller
    events.on("task_schedule", on_taskSchedule)
    
    # 添加插件机制，要在初始化路由前初始化插件
    from ._plugin import load_plugins
    load_plugins(app)
    
    tasker.start()

    from .models import db
    app.m_events.trigger('beforeCreateDb', eventArgs = db)
    db.create_all()
    init_routes(app)
    
    return app

def run_forever():
    if config.stream_log:
        import sspymgr.path_helper as ph
        ph.log_to_console = True
    if not config.webserver:
        logger.info("Webserver sspymgr webserver not start. Only shadowsocks will running")
        from .sscontroller import start_shadowsocks
        start_shadowsocks(wait=True)
        return

    if config.shadowsocks:
        from .sscontroller import start_shadowsocks
        start_shadowsocks()
    else:
        logger.info("shadowsocks won't start.")
    run_webserver()

def run_webserver():
    app = init_all()

    from gevent import pywsgi
    from .path_helper import createLogger

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

