# -*- coding: utf-8 -*-
from sspymgr.models import db
from datetime import datetime, timedelta

# class SaveFlow( db.db.Model ):
#     __tablename__ = 'saveFlow'
#     id = db.db.Column( db.db.Integer, primary_key = True, autoincrement = True )
#     port = db.db.Column( db.db.Integer )
#     flow = db.db.Column( db.db.BigInteger )
#     time = db.db.Column( db.db.DateTime )
#     accountId = db.db.Column( db.db.Integer )

# def genFlowRecord( tablename ):
#     def __repr__( self ):
#         return '<FlowRecord: %s>' % tablename

#     props = {
#         '__tablename__' : tablename,
#         'id' : db.Column( db.Integer, primary_key = True, autoincrement = True ),
#         'flow' : db.Column( db.BigInteger ),
#         'port' : db.Column( db.Integer ),
#         'time' : db.Column( db.DateTime ),
#         'accountId' : db.Column( db.Integer ),
#     }
#     newclass = type( tablename, ( db.Model, ), props )
#     return newclass

# FlowRecord = genFlowRecord( 'flowRecord' )
# FlowRecord5Min = genFlowRecord( 'flowRecord5min' )
# FlowRecordHour = genFlowRecord( 'flowRecordHour' )
# FlowRecordDay  = genFlowRecord( 'flowRecordDay' )


class FlowRecord5Min(db.Model):
    __tablename__ = 'flowRecord_5min'
    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer)
    flow = db.Column(db.Integer)  # unit of bytes
    date = db.Column(
        db.String, nullable=False)  # store date in the format: 2018-10-10
    hour = db.Column(db.Integer, nullable=False)  # 0 - 23
    minute = db.Column(
        db.Integer, nullable=False
    )  # noraml minute here, gap is 5, from 0 to 55: 0 ==> [ 00:00 ~ 04:59 ]

    @staticmethod
    def genRecord(port: int, flow: int, time: datetime):
        """time is record time, but should be 
        """
        d = '{:%Y-%m-%d}'.format(time)
        record = FlowRecord5Min(
            port=port, flow=flow, date=d, hour=time.hour, minute=time.minute)
        db.session.add(record)

    def to_dict(self):
        di = {
            'flow': self.flow,
            'hour': self.hour,
            'minute': self.minute
        }
        return di

    def __repr__(self):
        return '<FlowRecord5Min %d: %d at %s %d>' % (self.port, self.flow,
                                                     self.date, self.hour)


from sqlalchemy import func
from sqlalchemy.sql import label


class FlowRecordDay(db.Model):
    __tablename__ = 'flowRecord_Day'
    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer)
    flow = db.Column(db.Integer)  # unit of bytes
    date = db.Column(
        db.String,
        nullable=False)  # store date in the format (year and month): 2018-10
    day = db.Column(db.Integer, nullable=False)  # store day, from 1 to 31

    def to_dict(self):
        di = {
            'flow': self.flow,
            'day': self.day,
        }
        return di

    def __repr__(self):
        return '<FlowRecordDay %d: %d at %s %d>' % (self.port, self.flow,
            self.date, self.day)

    @staticmethod
    def genRecord(port: int, flow: int, time: datetime):
        """time is record time, but should be 
        """
        date = '{:%Y-%m}'.format(time)
        record = FlowRecordDay(port=port, flow=flow, date=date, day=time.day)
        db.session.add(record)

from .utils import logger
class FlowStats(object):
    """统计流量，将流量记录到数据库中
    """

    def __init__(self, *args, **kwargs):
        self.min = {}
        # self.hour = {}
        self.day = {}
        return super().__init__(*args, **kwargs)

    def recordFlow(self, accFlow: dict):
        """将流量数据记录到 dict 中
        accFlow: { 
            45001: {'flow': 12, 'status': 'added' }, 
            45002: {...}  
        }
        """
        for port, detail in accFlow.items():
            if port not in self.min:
                self.min[port] = detail['flow']
            else:
                self.min[port] = self.min[port] + detail['flow']
        # logger.debug("5 min: {}".format(self.min))
        for port in self.min:
            if port not in self.day:
                self.day[port] = self.min[port]
            else:
                self.day[port] += self.min[port]

    def record5minToDb(self):
        # logger.debug("5 min record: {}".format(str(self.min)))
        for port in self.min:
            if self.min[port] == 0:
                # no need to record
                continue
            FlowRecord5Min.genRecord(port, self.min[port], datetime.now())
            self.min[port] = 0
        db.session.commit()

    def record1hourToDb(self):
        pass

    def record1dayToDb(self):
        # FlowRecordDay.genRecordFrom5min( now )
        for port in self.day:
            if self.day[port] == 0:
                continue
            FlowRecordDay.genRecord(port, self.day[port], datetime.now())
            self.day[port] = 0
        db.session.commit()

from datetime import datetime, timedelta

from sspymgr import formatTime
from sspymgr.models import db
from sspymgr.sscontroller import Account, AccountFlow
from sspymgr.globalvars import emailManager
from web_user import User, UserType
import logging
logger = logging.getLogger("plugin_sscontroller")

def checkAllAccounts():
    """Action: check accounts status and userType
    """
    dbaccounts = Account.query.all()
    # accountFlow = AccountFlow.query.all()
    for acc in dbaccounts:
        # for flow in accountFlow:
        #     if acc.port == flow.port:
        #         acc._flow = flow
        #         break
        # if acc.is_valid():
        uid = acc.userId
        user = User.query.filter_by(id=uid).first()
        if user is None:
            continue
        now = datetime.now()
        if now < acc.expire: 
            if canSendLastDay(user) and (acc.expire - now) < timedelta(days=1):
                sendLastDay(acc)
        else:
            user.type = UserType.INVALID.value
            db.session.commit()
    

def sendLastDay(acc: Account, user: User):
    logger.debug("<{} : {}> will expire soon".format(user.email, user.comment))

    content = """Hi, your account of SSPY-MGR will be expired within one day (at {}).<br />
    Please go to {} to rechart Your account.(Your ss account Port: {})
    """.format(formatTime(acc.expire), acc.server, acc.port)
    user.type = UserType.NOTIFIED.value
    subject = "账户过期提醒"

    emailManager.add_email(
        to=user.email,
        subject=subject,
        content=content,
        type="last day notify")


def canSendLastDay(user):
    if user.type is None or len(user.type) == 0:
        return False
    utype = UserType(user.type)
    if (utype == UserType.BANNED or utype == UserType.TRIAL):
        return False
    if (utype != UserType.NOTIFIED):
        return True
    return False