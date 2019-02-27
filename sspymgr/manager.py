from flask import Flask

from .dbsessions import replaceSessionInterface

from .configuration import defaultConfig
from .models import createDatabase
from .mail import init as initEmail
from ._plugin import load_plugins

from .mail import EmailManager
from .sscontroller import SSController

import threading
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


class Manager(Flask):
    """Sub class of Flask, it would support better interface 
    .. Properties:: global variables
        m_config: Config which is set by configuration file or sys.argv
        m_db: sqlalchemy, database reference
        m_events: plugin.Events, events control and trigger
        m_tasker: plugin.BackTask, run background tasks such as shadowsocks flow stats
        m_sscontroller: sscontroller which is used to communicate with shadowsocks server
        m_emailManager: emailManager which is used to send and record email
    """
    m_config = None
    m_db = None
    m_events = None
    # EmailManager
    m_emailManager = None
    # SSController
    m_ssctronller = None

    def __init__(self, *args, **kwargs):
        """initialize all variables and databases.
        return a Flask instance app.
        """
        super().__init__(*args, **kwargs)
        self.__prepare()
        replaceSessionInterface(self)

    def start(self):
        """make everythin prepared and then run the manager
        """
        initEmail(self)

        self.m_events.on("task_schedule", self.scheduleTasks)
        
        # introduce plugin system, plugins should be inited before routes
        load_plugins(self)
        self.m_events.trigger('beforeCreateDb', eventArgs = self.m_db)
        self.m_db.create_all()
        self.m_events.trigger('afterCreateDb', eventArgs = self.m_db)
        self.m_sscontroller.start()
        
        self.init_routes()
        self.m_tasker.start()

    def scheduleTasks(self, schedule):
        schedule.every().seconds.do(run_threaded, self.m_emailManager.checkRemain)
        schedule.every().seconds.do(run_threaded, self.m_sscontroller.execute)
        self.logger.debug("Email and SSController is scheduled")
        

    def __prepare(self):
        from .path_helper import createLogger
        from ._plugin import Events, BackTask
        self.m_config = defaultConfig()
        self.m_db = createDatabase(self.m_config.database)
        self.logger = createLogger("sspymgr")

        self.m_events = Events()
        self.m_tasker = BackTask(self.m_events)

        self.m_emailManager = EmailManager(self.m_config, self.m_db)

        self.m_sscontroller = SSController(self.m_db)

    def init_routes(self):
        # from .routes.vuefront import vuefront

        @self.teardown_request
        def teardownd_database(resp):
            self.m_db.session.close()
            return resp

        from .routes import api
        # register core plugins and other plugins
        self.m_events.trigger('beforeRegisterApi', eventArgs = api )

        # add api routes which will start as `/api`
        self.register_blueprint( api, url_prefix='/api')
    