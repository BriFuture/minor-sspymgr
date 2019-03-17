# -*- coding: utf-8 -*-
"""Provide database model and routes as core plugin
"""

from .web_settings import WebguiSetting, registerApi as registerApiSetting
from .web_user import User, UserType, registerApi as registerApiUser,\
    getSuperManager, isManager, getCurrentUser
from .mail import EmailManager, registerApi as registerApiMail
from .routes import api

from sspymgr.manager import Manager
app = None

def init(iapp: Manager):
    global app
    app = iapp
    registerApiSetting(api, app)
    registerApiUser(api, app)
    app.m_emailManager = EmailManager(app.m_config, app.m_db)
    registerApiMail(api)