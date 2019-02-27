# -*- coding: utf-8 -*-
from sspymgr.models import DB
from datetime import datetime, timedelta

# class SaveFlow( DB.DB.Model ):
#     __tablename__ = 'saveFlow'
#     id = DB.DB.Column( DB.DB.Integer, primary_key = True, autoincrement = True )
#     port = DB.DB.Column( DB.DB.Integer )
#     flow = DB.DB.Column( DB.DB.BigInteger )
#     time = DB.DB.Column( DB.DB.DateTime )
#     accountId = DB.DB.Column( DB.DB.Integer )

# def genFlowRecord( tablename ):
#     def __repr__( self ):
#         return '<FlowRecord: %s>' % tablename

#     props = {
#         '__tablename__' : tablename,
#         'id' : DB.Column( DB.Integer, primary_key = True, autoincrement = True ),
#         'flow' : DB.Column( DB.BigInteger ),
#         'port' : DB.Column( DB.Integer ),
#         'time' : DB.Column( DB.DateTime ),
#         'accountId' : DB.Column( DB.Integer ),
#     }
#     newclass = type( tablename, ( DB.Model, ), props )
#     return newclass

# FlowRecord = genFlowRecord( 'flowRecord' )
# FlowRecord5Min = genFlowRecord( 'flowRecord5min' )
# FlowRecordHour = genFlowRecord( 'flowRecordHour' )
# FlowRecordDay  = genFlowRecord( 'flowRecordDay' )


class FlowRecord5Min(DB.Model):
    __tablename__ = 'flowRecord_5min'
    id = DB.Column(DB.Integer, primary_key=True)
    port = DB.Column(DB.Integer)
    # unit of bytes
    flow = DB.Column(DB.Integer)  
    # store date in the format: 2018-10-10
    date = DB.Column(DB.String, nullable=False) 
    # 0 - 23
    hour = DB.Column(DB.Integer, nullable=False)  
    # noraml minute here, gap is 5, from 0 to 55: 0 ==> [ 00:00 ~ 04:59 ]
    minute = DB.Column(DB.Integer, nullable=False) 

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

from datetime import datetime, timedelta

from sspymgr import formatTime
from sspymgr.sscontroller import Account, AccountFlow
from web_user import User, UserType
import logging
logger = logging.getLogger("plugin_sscontroller")


class FlowRecordDay(DB.Model):
    __tablename__ = 'flowRecord_Day'
    id = DB.Column(DB.Integer, primary_key=True)
    port = DB.Column(DB.Integer)
    flow = DB.Column(DB.Integer)  # unit of bytes
    date = DB.Column(
        DB.String,
        nullable=False)  # store date in the format (year and month): 2018-10
    day = DB.Column(DB.Integer, nullable=False)  # store day, from 1 to 31

    def to_dict(self):
        di = {
            'flow': self.flow,
            'day': self.day,
        }
        return di

    def __repr__(self):
        return '<FlowRecordDay %d: %d at %s %d>' % (self.port, self.flow,
            self.date, self.day)


from . import logger
class FlowStats(object):
    """统计流量，将流量记录到数据库中
    """
    MINUTE = 5

    def __init__(self, db, *args, **kwargs):
        self.db = db
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
        for port in self.min:
            if port not in self.day:
                self.day[port] = self.min[port]
            else:
                self.day[port] += self.min[port]

        logger.debug("5 min: {}".format(self.min))

    def record5minToDb(self):
        now = datetime.now()
        cond = (now.minute + 1) % self.MINUTE
        if( cond != 0 ):
            return
        gen = 0
        for port in self.min:
            if self.min[port] == 0:
                # no need to record
                continue
            self.genMinRecord(port, self.min[port], now)
            self.min[port] = 0
            gen += 1
        logger.debug("5 min record to db count: {}".format(gen))
        self.db.session.commit()

    def record1hourToDb(self):
        pass

    def record1dayToDb(self):
        gen = 0
        for port in self.day:
            if self.day[port] == 0:
                continue
            self.genDayRecord(port, self.day[port], datetime.now())
            self.day[port] = 0
            gen += 1
        logger.debug("day record to db count: {}".format(gen))
        self.db.session.commit()

    def genMinRecord(self, port: int, flow: int, time: datetime):
        """time is record time, but should be 
        """
        d = '{:%Y-%m-%d}'.format(time)
        record = FlowRecord5Min(
            port=port, flow=flow, date=d, hour=time.hour, minute=time.minute)
        self.db.session.add(record)
        return record

    def genDayRecord(self, port: int, flow: int, time: datetime):
        """time: record time
        """
        date = '{:%Y-%m}'.format(time)
        record = FlowRecordDay(port=port, flow=flow, date=date, day=time.day)
        self.db.session.add(record)
        return record
        

class AccountsChecker(object):
    app = None
    def __init__(self, app, *args, **kwargs):
        self.app = app

    def checkAllAccounts(self):
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
                if self.canSendLastDay(user) and (acc.expire - now) < timedelta(days=1):
                    self.sendLastDay(acc, user)
            else:
                user.type = UserType.INVALID.value
            
        self.app.m_db.session.commit()
        
    # from 
    def sendLastDay(self, acc: Account, user: User):
        logger.debug("<{} : {}> will expire soon".format(user.email, user.comment))

        # content = """Hi, your account of SSPYMGR will be expired within one day (at {}).<br />
        # Please go to {} to rechart Your account.(Your ss account Port: {})
        # """.format(formatTime(acc.expire), acc.server, acc.port)
        content = """你好, 你的 SSPYMGR 账户将会在一天后过期 (即 {}).<br />
        请访问 {} 以重新激活你的账户.(你的 shadowsocks 账号端口是: {})
        """.format(formatTime(acc.expire), acc.server, acc.port)
        user.type = UserType.NOTIFIED.value
        subject = "账户过期提醒"
        self.app.m_emailManager.add_email(
            to=user.email,
            subject=subject,
            content=content,
            type="last day notify")


    def canSendLastDay(self, user):
        if user.type is None or len(user.type) == 0:
            return False
        utype = UserType(user.type)
        if (utype == UserType.BANNED or utype == UserType.TRIAL):
            return False
        if (utype != UserType.NOTIFIED):
            return True
        return False