import hashlib, random, string
code_lib = string.ascii_letters + string.digits

import re
EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

def isEmailMatched(email: str) -> bool:
    return EMAIL_REGEX.match(email)

def getRandomCode( bit = 6 ) -> str:
    return ''.join( random.SystemRandom().choices( code_lib, k = bit ) )

def convertFlowToByte( flow: int, unit: string ):
    """
    convert flow into bytes
    @param unit: UpperCase, could be G, M, K
    """
    if unit == 'GB' or unit == 'G':
        return flow * 1024 * 1024 * 1024
    elif unit == 'MB' or unit == 'M':
        return flow * 1024 * 1024
    elif unit == 'KB' or unit == 'K':
        return flow * 1024
    
    return flow

def convertByteToFlow( bytes: int ):
    # if bytes < 1024:
    #     return '%d b' % bytes
    # elif bytes < 1024 * 1024:
    #     return '%d Kb' % bytes / 1024
    mb = bytes / 1024 / 1024
    if mb < 1024:
        return '%d Mb' % mb

    gb, mb = divmod( mb, 1024 )
    if mb != 0:
        return '%d Gb %d Mb' % ( gb, mb )
    else:
        return '%d Gb' % gb

from datetime import datetime
def formatTime( dt: datetime ):
    """given datetime object, return string format, 
    second will be hide
    """
    return dt.strftime( '%Y-%m-%d %H:%M' )

def second2str( seconds: int ):
    days, remains = divmod( seconds, 86400 )
    hours, remains = divmod( remains, 3600 )
    minutes, remains = divmod( remains, 60 )
    str = ''
    if days != 0:
        str += "%d days" % days
    if hours != 0:
        str += "%d hours" % hours
    if minutes != 0:
        str += "%d minutes" % minutes
    return str

def mbflow2str( flow: int ):
    """unit of flow is MB
    """
    str = None
    if flow < 1024:
        return '%d Mb' % flow

    gb, mb = divmod( flow, 1024 )
    if mb != 0:
        return '%d Gb %d Mb' % ( gb, mb )
    else:
        return '%d Gb' % gb

from pathlib import Path

LANGUAGE_DIR = (Path(__file__).parent / "locale").resolve()

import gettext
def initGettext(domain="sspymgr") -> gettext.gettext:
    """make some configurations on gettext module 
    for convenient internationalization
    """
    gettext.bindtextdomain(domain, LANGUAGE_DIR)
    gettext.textdomain(domain)
    gettext.find(domain, "locale", languages=["zh_CN", "en_US"])
    return gettext.gettext