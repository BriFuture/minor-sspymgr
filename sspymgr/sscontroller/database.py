# -*- coding: utf-8 -*-

from sspymgr.models import db
from datetime import datetime, timedelta


class Account(db.Model):
    """
    Represents shadowsocks server account, port and password can not be None
    """
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # corresponding with Table User, but can be created by manager
    userId = db.Column(db.Integer, unique=True)  
    data = db.Column(db.String(255))
    port = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    totalFlow = db.Column(db.BigInteger)
    expire = db.Column(db.DateTime)
    server = db.Column(db.String(255))
    method = db.Column(db.String(64), default='aes-256-cfb')
    # server = db.Column( db.String( 255 ) )  # no need for multi server now
    """
    @field type
        0 registered by email and have a 
    """
    type = db.Column(db.Integer)
    status = db.Column(db.String(32))
    createTime = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)

    def get_status(self):
        if self.status == 0:
            return 0
        return 0

    def is_valid(self):
        now = datetime.now()
        if now > self.expire:
            return False
        # accountFlow = AccountFlow.query.filter_by( accountId = self.id ).first()
        flow = self._flow.flow
        if flow > self.totalFlow:
            return False
        return True

    def clear_flow(self):
        self._accountFlow.flow = 0
        self._flow.flow = 0
        db.session.commit()

    def get_used_flow(self):
        if hasattr(self, '_flow'):
            return self._flow.flow
        return None

    def __repr__(self):
        return '<Account %d>' % self.id

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


class AccountFlow(db.Model):
    __tablename__ = 'accountFlow'

    port = db.Column(db.Integer, primary_key=True)
    flow = db.Column(db.BigInteger, default=0)  # flow used
    status = db.Column(db.String(255), default='checked')
    accountId = db.Column(db.Integer, unique=True)
    updateTime = db.Column(
        db.DateTime, default=datetime.now)  # means the account last connected
    autoBanTime = db.Column(db.DateTime)

    # serverId  = db.Column( db.Integer )
    checkTime = db.Column(db.DateTime)
    nextCheckTime = db.Column(db.DateTime)

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


class Command(db.Model):
    __tablename__ = 'command'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    time = db.Column(db.String(255))

