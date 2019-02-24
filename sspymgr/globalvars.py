# -*- coding: utf-8 -*-

import re
EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

from .path_helper import createLogger

logger = createLogger("sspymgr")

from ._plugin import Events, BackTask
events = Events()
tasker = BackTask(events)

from .configuration import Configuration
config = Configuration()

from .mail import EmailManager
emailManager = EmailManager(config)

from .sscontroller import SSController
controller = SSController()
