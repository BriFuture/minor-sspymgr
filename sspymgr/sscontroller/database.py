# -*- coding: utf-8 -*-

from sspymgr.models import DB
from datetime import datetime, timedelta


class Account(DB.Model):
    """
    Represents shadowsocks server account, port and password can not be None
    """
    __tablename__ = 'account'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    # corresponding with Table User, but can be created by manager
    userId = DB.Column(DB.Integer, unique=True)  
    data = DB.Column(DB.String(255))
    port = DB.Column(DB.Integer, nullable=False)
    password = DB.Column(DB.String(255), nullable=False)
    totalFlow = DB.Column(DB.BigInteger)
    expire = DB.Column(DB.DateTime)
    server = DB.Column(DB.String(255))
    method = DB.Column(DB.String(64), default='aes-256-cfb')
    # server = DB.Column( DB.String( 255 ) )  # no need for multi server now
    """
    @field type
        0 registered by email and have a 
    """
    type = DB.Column(DB.Integer)
    status = DB.Column(DB.String(32))
    createTime = DB.Column(DB.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)

    def get_status(self):
        if self.status == 0:
            return 0
        return 0

    def is_flow_remaining(self):
        """If this account has remaining flow, True returned, otherwise False.
        """
        if not hasattr(self, 'account_flow'):
            self.account_flow = AccountFlow.query.filter_by(port=self.port).first()
        return self.totalFlow > self.account_flow.flow

    def clear_flow(self):
        """Clear flow usage stats
        """
        if not hasattr(self, 'account_flow'):
            self.account_flow = AccountFlow.query.filter_by(
                port=self.port).first()
        self.account_flow.flow = 0

    def get_used_flow(self):
        if hasattr(self, '_flow'):
            return self._flow.flow
        return None

    def __repr__(self):
        return '<Account {} status: {}>'.format(self.port, self.status)

    def to_dict(self):
        di = {
            'id': self.id,
            'userId': self.userId,
            'data': self.data,
            'port': self.port,
            'password': self.password,
            'totalFlow': self.totalFlow,
            'usedFlow': self.get_used_flow(),
            'server': self.server,
            'method': self.method,
            'type': self.type,
            'status': self.status,
            'expire': self.expire.timestamp(),
            'createTime': self.createTime.timestamp(),
        }
        return di


class AccountFlow(DB.Model):
    __tablename__ = 'accountFlow'

    port = DB.Column(DB.Integer, primary_key=True)
    flow = DB.Column(DB.BigInteger, default=0)  # flow used
    status = DB.Column(DB.String(255), default='checked')
    accountId = DB.Column(DB.Integer, unique=True)
    updateTime = DB.Column(
        DB.DateTime, default=datetime.now)  # means the account last connected
    autoBanTime = DB.Column(DB.DateTime)

    # serverId  = DB.Column( DB.Integer )
    checkTime = DB.Column(DB.DateTime)
    nextCheckTime = DB.Column(DB.DateTime)

    def consume_flow(self, flow: int):
        self.flow += flow
        self.updateTime = datetime.now()

    def __repr__(self):
        return '<Flow port: %d, flow: %d>' % (self.port, self.flow)

    def to_dict(self):
        di = {
            'port': self.port,
            'flow': self.flow,
            'status': self.status,
            'accountId': self.accountId,
            'updateTime': self.updateTime.timestamp(),
            'autoBanTime': self.autoBanTime.timestamp(),
            'checkTime': self.checkTime.timestamp(),
            # 'nextCheckTime': self.nextCheckTime.timestamp(),
        }
        return di


class Command(DB.Model):
    __tablename__ = 'command'
    id = DB.Column(DB.Integer, primary_key=True)
    code = DB.Column(DB.String(255))
    time = DB.Column(DB.String(255))

