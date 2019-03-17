# -*- coding: utf-8 -*-
"""Description: This module is used for communicate with shadowsocks server, it contains basic protocol 
which defines how to communicate with shadowsocks server. Also contains a controller class to provide 
convenient methods for other modules.

Author: BriFuture

Detail: 2019/03/17 12:31
"""

DEFAULT_METHOD = "aes-256-cfb"
from .utils import logger

def _ping():
    """Return a tuple that is made up of a message that need to be sent to shadowsocks server 
    and the expected response from shadowsocks server
    """
    return b'ping', b'pong'

def _add_port(port, password, method):
    """Return a tuple that contains 4 elements
    First:  is the message that should be sent to shadowsocks server;
    Second: is the expected response from shadowsocks server;
    Third:  is a bool type value which indicates whether it is account-add operation.
    Fourth: is the port passed in.
    """
    cmd = 'add: {{ "server_port": {:d}, "password": "{:s}", "method": "{:s}" }}'.format(port, password, method)
    return cmd.encode( 'ascii' ), b'ok', True, port

def _remove_port(port):
    """Return a tuple that contains 4 elements, the same as ``_add_port``
    """
    cmd = 'remove: {{ "server_port": {:d} }}'.format(port)
    return cmd.encode( 'ascii' ), b'ok', False, port

# import re
# STAT = re.compile( b'stat: {[^s]+}' )
import json
from queue import Queue
from time import sleep
from .database import Account, AccountFlow
import socket 
# from gevent import socket, spawn, joinall
# from gevent.pool import Pool

class SSAdapter( object ):
    """Socket layer operation, it contains a queue which contains commands (ping or add_port or remove_port) that wait to be sent, 
    Pass a stater callback function as constructor parameter, and it will be called every time when shadowsocks statistics comes.

    Account States: created -> adding -> added -> invalid -> removed -> recreate
    accounts is a dict, contains port and flow.
    ..python::
        accounts = { 
            45000: Account, 
            45001: Account
        }
    """
    StateCreated = "created"
    StateAdding = "adding"
    StateAdded = "added"
    StateRemoving = "removing"
    StateRemoved  = "removed"
    StateRecreate = "recreate"
    ValidStates = ("adding", "added")
    InvalidStates = ("removed", "removing")
    MaxStatCount = 15

    def __init__( self, stater ):
        """``stater`` is the callback function which would be triggered every time shadowsocks server 
        send statistic messages.
        """
        # key is port: int, value is Account object
        self.accounts = dict()
        self._db = None
        self._stater = stater
        self._queue = Queue()
        self._stat_count = 0

    def conn_ser( self, server ):
        """Connect to shadowsocks server, ``server`` can be either a tuple for example ('127.0.0.1', 6060), either a str which is the location of unix sock file

        Note:
            unix sock file mode is not usable currently
        """
        # create a socket object, generally no exception here
        if type( server ) is tuple:
            self._socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )  ## UDP connection
        else:
            self._socket = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )

        self._socket.settimeout( 0 )  # never timeout
        self._socket.setblocking( False ) # none block
        try:
            self._socket.connect( server )
        except OSError as e:
            logger.critical("Error when connecting to shadowsocks server: {}".format(e))

        # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ping()

    def ping( self ):
        """Tell the adapter to check whether shadowsocks server is online.
        """
        cmd = _ping()
        self._queue.put( cmd )

    def add_port( self, account: Account ):
        """Add an shadowsocks account with ``port``, ``password`` and ``method``
        accounts status process: created -> added
        """
        if account.port in self.accounts:
            self.accounts[account.port].status = self.StateRecreate
        else:
            self.accounts[account.port] = account
            account.status = self.StateCreated
        if account.status in self.ValidStates:
            # logger.info("Account {} is added, no need to duplicate add_port.".format(account))
            return
        cmd = _add_port(account.port, account.password, account.method)
        self._queue.put( cmd )
        logger.info("port is adding : {}".format(cmd))
    
    def remove_port( self, account: Account ):
        """Remove ``port`` from shadowsocks server, 
        accounts status process: removing => removed
        """
        if account.port not in self.accounts:
            self.accounts[account.port] = account
            
        account.totalFlow = 0
        account.clear_flow()
        if account.status in self.InvalidStates:
            logger.info("Account {} not valid, no need to remove_port.".format(account))
            return
        account.status = self.StateRemoving
        cmd = _remove_port(account.port)
        self._queue.put( cmd )
        logger.info("Port is removing : {}".format(cmd))
    
    def update_port( self, account: Account):
        """Convenient function for update ``password`` and ``method`` of account in shadowsocks server.
        """
        self.remove_port( account )
        self.add_port( account )

    def is_port_valid( self, port: int ):
        """Check if a port has been activated by the shadowsocks server
        """
        if port in self.accounts:
            return self.accounts[port].status == self.StateAdded
        return False

    def execute(self):
        """1. Check remaining commands in command queue and send them, 2. Recv message coming from shadowsocks server 
        """
        cmd = None
        if not self._queue.empty():
            cmd = self._queue.get()
            self._socket.send( cmd[0] )
            logger.debug("[sending]: {}".format(cmd))
            sleep(0.01)
        rmsg = None
        try:
            rmsg = self._socket.recv( 2048 )
            self._stat_count = 0
        except Exception as exc:
            if type(exc) != BlockingIOError:
                logger.warn("cmd executing error: {}".format(exc) )
        finally:
            self._stat_count += 1
            if( self._stat_count == self.MaxStatCount ):
                # avoid long time not recved stats information
                # logger.debug("SSServer not response for a long time")
                self._stater(self.accounts)
                self._stat_count = 0
                
        if rmsg is None:
            return
        isstat = rmsg[:4] == b'stat'
        if isstat:
            stats = rmsg[5:]
            stats = json.loads( stats )
            for key in stats:
                account = self.accounts[ int( key ) ]
                account.used_flow += stats[ key ]
            self._stater(self.accounts)
        else:
            if cmd is None:
                logger.info("Recv unrecognized message: {}".format(rmsg))
            else:
                self._process_response(rmsg, cmd)
                logger.debug("resp: {} cmd: {}".format(rmsg, cmd))


    def _process_response(self, rmsg, cmd):
        if rmsg != cmd[1]:
            logger.debug('recv msg: {} did not matchs expected: {}'.format(rmsg, cmd[1]))
            return

        if len(cmd) < 3:
            logger.info( 'Recved Pong from server' )
            return

        add = cmd[ 2 ]
        port = cmd[ 3 ]
        account = Account.query.filter_by(port = port).first()
        # account = self.accounts[port]
        account.status = self.StateAdded if add else self.StateRemoved
        account.used_flow = self.accounts[port].used_flow
        self._db.session.commit()
        self.accounts[port] = account
        logger.info( 'port {} is added: {}'.format(account, add) )

    def _process_stats(self):
        pass


from datetime import datetime, timedelta

GB = 1024 * 1024 *1024 # unit: bytes

class SSController(object):
    """Provide advanced api for manipulating shadowsocks server.
    """

    def __init__(self, db):
        """Start running the adapter that corresponds to communicate with shadowsocks server
        """
        self._db = db
        self._stats = None
        from .utils import ssAddr
        adapter = SSAdapter( self.process_stats )
        adapter._db = db
        adapter.conn_ser( server = ssAddr() )
        self._adapter = adapter
        self._started = False

    def _start(self):
        # append account to shadowsocks server
        dbaccounts = Account.query.all()
        accountFlow = AccountFlow.query.all()
        now = datetime.now()
        for acc in dbaccounts:
            # attach accountFlow object to account
            for flow in accountFlow:
                if acc.port == flow.port:
                    acc.account_flow = flow
                    break
            # acc.status = SSAdapter.StateCreated
            acc.used_flow = 0
            # add port for this account no matter what state the account is (valid or invalid), 
            self._adapter.add_port(acc)

        self._db.session.commit()

    def setStats(self, stats):
        self._stats = stats

    def process_stats(self, accounts: dict):
        # if stats callback function is set, call it
        if self._stats is not None:
            self._stats({port: account.used_flow for port, account in accounts.items()})
        now = datetime.now()
        dbaccounts = Account.query.all()
        accountFlow = AccountFlow.query.all()
        now = datetime.now()
        for account in dbaccounts:
            # attach accountFlow object to account
            for flow in accountFlow:
                if account.port == flow.port:
                    account.account_flow = flow
                    break
        
            # iterate all accounts stored in database records
            raw_account = accounts[account.port]
            account.used_flow = raw_account.used_flow
            if account.status in SSAdapter.ValidStates and account.used_flow != 0:
                account.account_flow.updateTime = datetime.now()
                account.account_flow.flow += account.used_flow
                account.used_flow = 0
            if now > account.expire or not account.is_flow_remaining():
                # account is invalid now
                self._adapter.remove_port(account)
            elif account.status in SSAdapter.StateRemoved:
                self._adapter.add_port(account)
        self._db.session.commit()


    def add_account(self, port, password, flow = GB, **kwargs):
        """add a non-existing account to shadowsocks server, for existing accounts just 
        activate them will be fine
        @params 
            port: int = None
            password: str = None
            flow in the unit of byte,
            expire 
        @returns bool True if successfully added
        """
        if port in self._adapter.accounts:
            # Account already exists
            return False 
        # create account and record
        account = Account(port=port, password=password,
            # default flow: 1G
            totalFlow=flow,
            userId=kwargs.get("userId"),
            expire=kwargs.get("expire"),
            method = kwargs.get("method", DEFAULT_METHOD)
        )
        flow = AccountFlow(port=port, updateTime=now, checkTime=now, 
            autoBanTime = kwargs.get("expire"))
        account.account_flow = flow
        self._adapter.add_port(account)
        now = datetime.now()

        self._db.session.add(account)
        self._db.session.add(flow)
        self._db.session.commit()
        return True

    def del_account(self, port, **kwargs):
        """Delete an account in shadowsocks server, wont affect records in database
        """
        account = Account.query.filter_by(port=port).first()
        self._adapter.remove_port(account)
        self._db.session.commit()

    def get_account_by_id(self, id):
        """Return the account object if found, or None
        """
        # for port, account in self._adapter.accounts.items():
        #     if account.id == id:
        #         return account
        # return None
        account = Account.query.filter_by(id=id).first()
        if account is not None:
            account_flow = AccountFlow.query.filter_by(port = account.port).first()
            account.account_flow = account_flow
        return account

    def get_account_by_uid(self, uid) -> Account:
        """Return the account object if found, or None
        """
        # for port, account in self._adapter.accounts.items():
        #     if account.userId == uid:
        #         return account
        # return None
        account = Account.query.filter_by(userId=uid).first()
        if account is not None:
            account_flow = AccountFlow.query.filter_by(port = account.port).first()
            account.account_flow = account_flow
        return account

    def get_account_by_port(self, port) -> Account:
        """Return the account object if found, or None
        """
        # account = None
        # if port in self._adapter.accounts:
        #     account = self._adapter.accounts[port]
        # return account
        account = Account.query.filter_by(port=port).first()
        if account is not None:
            account_flow = AccountFlow.query.filter_by(port = account.port).first()
            account.account_flow = account_flow
        return account

    def update_totalflow(self, account: Account, bytes_flow: int):
        """Clear the flow usage on account, and update only ``totalFlow`` property of the account
        Note: ``db.session.commit`` has to be invokde by the caller
        """
        account.totalFlow = bytes_flow
        account.clear_flow()
        if not self._adapter.is_port_valid(account.port):
            self._adapter.add_port(account)
        return True

    def update_validity(self, account: Account, seconds: int, from_today=False):
        """Update validity property of an account 
        Note: ``db.session.commit`` has to be invokde by the caller
        @Return True indicate the port will be added, False removed
        """
        td = timedelta(seconds=seconds)
        now = datetime.now()
        if from_today:
            account.expire = now
        account.expire += td

        if account.expire > now:
            self._adapter.add_port(account)
            return True
        else:
            self._adapter.remove_port(account)
            return False

    def update_password(self, password, port=0, uid=None):
        """@deprecated Use update_password_by_port or update_password_by_uid instead.
        Update password of shadowsocks account. If ``uid`` is set, it's preferred be used to match the accounts;
        If ``port`` and ``uid`` are both set, it will check whther passed port matches the port in database record.
        Ohterwise, no action will be applied, False returned
        @returns True for success, False for failure
        """
        if uid is None:
            account = Account.query.filter_by(port=port).first()
        else:
            account = Account.query.filter_by(userId=uid).first()
            if port != 0 and account.port != port:
                return False
        if not account:  # in case account not found
            return False
        self._adapter.update_port(account)
        account.password = password
        self._db.session.commit()
        return True

    def update_password_by_port(self, password, port):
        """Update password of account(port identified)
        """
        account = Account.query.filter_by(port=port).first()
        return self._update_password(account, password)

    def update_password_by_uid(self, password, uid):
        """Update password of account(uid identified)
        """
        account = Account.query.filter_by(userId=uid).first()
        return self._update_password(account, password)

    def _update_password(self, account, password):
        if not account:  # in case account not found
            return False
        self._adapter.update_port(account)
        account.password = password
        self._db.session.commit()
        return True

    def execute(self):
        """send command and recieve message
        """
        if not self._started:
            self._start()
            self._started = True
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

    def renew_account(self, flow, duration, port=None, uid=None):
        """@deprecated Use ``update_flow_validity`` instead
        Renew an account with total flow and validity
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
        self._update_account(acc, flow = flow, expire = expire)
        self._db.session.commit()
        return True

    def _update_account(self, acc, expire: datetime = None, flow = GB):
        """@param acc: account
        """
        accFlow = AccountFlow.query.filter_by(port=acc.port).first()
        # A problem here is that user may lose some flow if last order is still active
        accFlow.flow = 0
        acc.totalFlow = flow
        if expire is not None:
            acc.expire = expire
        ## communicate with shadowsocks
        self._adapter.update_port(acc)