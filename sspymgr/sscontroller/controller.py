# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

from .database import db, Account, AccountFlow
from .utils import logger, ssAddr
from .adapter import SSAdapter

class SSController(object):
    """Account: created -> added -> invalid -> removed
    """

    def __init__(self):
        self.stat_counter = 0
        self.stats = None

    def start(self):
        adapter = SSAdapter( self.process_stats )
        try:
            mgr_addr = ssAddr()
            adapter.conn_ser( server = mgr_addr )
        except Exception as exc:
            print( exc )
        self._adapter = adapter
        self.__load_accounts_fromdb()

    def setStats(self, stats):
        self.stats = stats

    def process_stats(self, accounts, force=False):
        if self.stat_counter >= 1 or force:
            if self.stats is not None:
                self.stats(accounts)
            # logger.debug("stats func: {}".format(self.stats))
            self._do_process_stats(accounts)
            self.stat_counter = 0
        self.stat_counter += 1

    def _do_process_stats(self, accounts):
        """@param accounts, send from ss adapter
        """
        dbaccounts = Account.query.all()
        accountFlow = AccountFlow.query.all()
        for acc in dbaccounts:
            p = acc.port
            for flow in accountFlow:
                if p == flow.port:
                    acc._flow = flow
                    break
            logger.debug("process stats: {}".format(accounts[p]))
            if p in accounts.keys() and accounts[p]['flow'] != 0:
                acc._flow.updateTime = datetime.now()
                acc._flow.flow += accounts[p]['flow']
                accounts[p]['flow'] = 0

            if not acc.is_valid():
                acc.totalFlow = 0
                acc._flow.flow = 0
                self._adapter.remove_port(p)
                acc.status = 'removed'
            else:
                if acc.status == 'removed':
                    self._adapter.add_port(p, acc.password)
                    acc.status = 'added'
            # logger.debug("process stats: {}".format(accounts[p]))
            # logger.debug( 'after statis: %d %d' % (acc.port, acc._flow.flow ) )
        db.session.commit()

    def __load_accounts_fromdb(self):
        """only called once after program restart
        """
        dbaccounts = Account.query.all()
        accountFlow = AccountFlow.query.all()
        for acc in dbaccounts:
            for flow in accountFlow:
                if acc.port == flow.port:
                    acc._flow = flow
                    break
            if acc.status == 'removed' or acc.status == 'invalid':
                if acc.is_valid():
                    self._adapter.add_port(acc.port, acc.password)
                    acc.status = 'added'
            elif acc.status == 'added':
                self._adapter.add_port(acc.port, acc.password)

    def add_account(self, port, password, **kwargs):
        """
        @params 
            port: int = None
            password: str = None
            flow in the unit of byte,
            expire 
        @returns bool True if successfully added
        """
        if port in self._adapter.accounts:
            return 'Account already exists'
        # create account
        account = Account(
            port=port,
            password=password,
            userId=kwargs.get('userId'),
            totalFlow=kwargs['flow'],
            expire=kwargs['expire'],
            status='added')
        now = datetime.now()
        flow = AccountFlow(port=port, updateTime=now, checkTime=now)
        flow.autoBanTime = kwargs['expire']

        db.session.add(account)
        db.session.add(flow)
        self._adapter.add_port(port, password)
        db.session.commit()
        return True

    def del_account(self, port, **kwargs):
        """delete an account in ss
        """
        self._adapter.remove_port(port)
        account = Account.query.filter_by(port=port).first()
        account.status = 'removed'
        accountFlow = AccountFlow.query.filter_by(port=port).first()
        db.session.delete(accountFlow)
        db.session.delete(account)
        db.session.commit()

    def get_account(self, id):
        account = Account.query.filter_by(id=id).first()
        if account is not None:
            accountFlow = AccountFlow.query.filter_by(
                port=account.port).first()
            account._flow = accountFlow
        return account

    def renew_account(self, flow, duration, port=None, uid=None):
        """renew an account with new flow and duration
        @param 
            flow: in unit byte
            duration: timedelta
        """
        if port:
            acc = Account.query.filter_by(port=port).first()
        elif uid:
            acc = Account.query.filter_by(userId=uid).first()
        else:
            return False

        # it will cause more time instead of less
        date = datetime.now()
        if date < acc.expire:
            date = acc.expire
        expire = duration + date
        self._update_account(acc, flow, expire)
        return True

    def _update_account(self, acc, flow: int = None, expire: datetime = None):
        """@param acc: account
        """
        accFlow = AccountFlow.query.filter_by(port=acc.port).first()
        # a problem here is that user may lose some flow if last order is active
        accFlow.flow = 0
        if flow is not None:
            acc.totalFlow = flow
        if expire is not None:
            acc.expire = expire
        acc.status = 'added'
        ## communicate with shadowsocks
        self._adapter.remove_port(acc.port)
        self._adapter.add_port(acc.port, acc.password)
        db.session.commit()
        return True

    
    def update_password(self, password, port=0, uid=None):
        """更新 Shadowsocks 账户密码
        若设置了 uid，则优先通过 userId 匹配账户，若同时设置 port 和 uid，则会检查 port 与 uid 是否匹配
        若 uid 和 port 都不设置，则不操作数据库，返回 False
        @returns True 更新成功， False 更新失败 
        """
        if uid is None:
            account = Account.query.filter_by(port=port).first()
        else:
            account = Account.query.filter_by(userId=uid).first()
            if port != 0 and str(account.port) != port:
                return False
        if not account:  # in case account not found
            return False
        self._adapter.update_port(account.port, password)
        account.password = password
        db.session.commit()
        return True

    def execute(self):
        """send command and recieve message
        """
        self._adapter.execute()

    def list_account(self, atype='all'):
        """
        @ param atype
            'all'   list of all accounts
            'valid' list of all valid accounts
            'invalid' list of all invalid accounts
        @returns
            a list with all account
        """
        dbaccounts = Account.query.all()
        accountFlow = AccountFlow.query.all()
        for acc in dbaccounts:
            for flow in accountFlow:
                if acc.port == flow.port:
                    acc._flow = flow
                    break
        return dbaccounts
