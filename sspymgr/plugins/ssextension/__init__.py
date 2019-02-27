# -*- coding: utf-8 -*-

from sspymgr import createLogger
logger = createLogger(
    "plugin_sscontroller", stream=True, logger_prefix="[Plugin sscontroller]")
from sspymgr import getRandomCode
from datetime import datetime, timedelta

app = None

from .flow_stats import AccountsChecker
from .flow_stats import FlowStats

import threading
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def scheduleTasks(schedule):
    recorder = FlowStats(app.m_db)
    app.m_sscontroller.setStats(recorder.recordFlow)
    schedule.every().minute.at(":57").do(run_threaded, recorder.record5minToDb)
    schedule.every().day.at("23:59").do(run_threaded,  recorder.record1dayToDb)
    accChecker = AccountsChecker(app)
    schedule.every().minutes.do(accChecker.checkAllAccounts)
    logger.debug("Tasks scheduled done")


from .ssc_routes import availiable_port


def afterSingup(params: dict):
    port = availiable_port(app.m_db)
    password = getRandomCode(8)
    from web_settings import WebguiSetting
    days = WebguiSetting.getSetting(key='web_signup_trial_days',\
            default_value=1, default_type="Number").getTypedValue()
    expire = timedelta(days=days) + datetime.now()
    added = app.m_sscontroller.add_account(
        port,
        password,
        userId=params['userId'],
        flow=params['flow'],
        expire=expire)
    logger.debug("signup accounts added: {}, params: {}".format(added, params))


from .ssc_routes import registerRoutes


def registerApi(api):
    registerRoutes(api, app)


from sspymgr import Manager


def init(iapp: Manager):
    global app
    app = iapp
    app.m_events.on('beforeRegisterApi', registerApi)
    app.m_events.on('task_schedule', scheduleTasks)
    app.m_events.on('webuser_signup_success', afterSingup)
    logger.info("inited")