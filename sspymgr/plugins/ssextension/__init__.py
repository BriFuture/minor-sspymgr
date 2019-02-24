# -*- coding: utf-8 -*-


from sspymgr import createLogger
logger = createLogger(
    "plugin_sscontroller", stream=False, logger_prefix="[Plugin sscontroller]")
from .ssc_routes import registerApi, availiable_port
from sspymgr.globalvars import config, controller
from sspymgr import getRandomCode
from datetime import datetime, timedelta

from .flow_stats import FlowStats, checkAllAccounts
def scheduleTasks(schedule):
    recorder = FlowStats()
    controller.setStats(recorder.recordFlow)
    for i in range(1, 13):
        schedule.every(1).hours.at(":{:02d}".format(i*5-1)).do(recorder.record5minToDb)
    schedule.every().day.at("23:59").do(recorder.record1dayToDb)
    schedule.every().minutes.do(checkAllAccounts)
    logger.debug("Tasks scheduled done")

def afterSingup(params: dict):
    port = availiable_port()
    password = getRandomCode(8)
    from web_settings import WebguiSetting
    days = WebguiSetting.getSetting(key='web_signup_trial_days',\
            default_value=1, default_type="Number").getTypedValue()
    expire = timedelta(days=days) + datetime.now()
    added = controller.add_account(
        port,
        password,
        userId=params['userId'],
        flow=params['flow'],
        expire=expire
    )
    logger.debug("signup accounts added: {}, params: {}".format(added, params))

def init(app):
    app.m_events.on('beforeRegisterApi', registerApi)
    app.m_events.on('task_schedule', scheduleTasks)
    app.m_events.on('webuser_signup_success', afterSingup)
    logger.info("inited")