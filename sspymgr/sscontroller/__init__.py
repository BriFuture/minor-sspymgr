# -*- coding: utf-8 -*-

"""Description: Used for control shadowsocks, for example: add account, del account, flow usage stats.
The method ``start_shadowsocks`` integrates shadowsocks into sspymgr and it will start a shadowsocks server
in a separate thread. ``ssAddr`` can be used to make sure that shadowsocks server and adapter communicate 
with the same address, either unix socks file, either socket.

Author: BriFuture

Date: 2019/03/19
"""

__version__ = "0.0.6"

from sspymgr import convertFlowToByte, getRandomCode, Manager, createLogger
from sspymgr.core import User, WebguiSetting, UserType
logger = createLogger('sscontroller', stream=False, logger_prefix="[Core SSController]")

from .database import Account, AccountFlow
from .adapter import SSController

import sys
def ssAddr(addr2str = False):
    """Get universal address for communicating with shadowsocks server
    """
    if sys.platform.startswith( 'linux' ):
        mgr_addr = '/var/run/sspymgr.sock'
    else:
        mgr_addr = ('127.0.0.1', 6001)

    # some problem in unix sock file, using tcp mode always currently
    mgr_addr = ('127.0.0.1', 6001)

    if addr2str:
        mgr_addr = '{}:{}'.format( mgr_addr[0], mgr_addr[1])
    return mgr_addr

from .run_ss import main as start_shadowsocks

app = None
def init(iapp: Manager):
    global app
    app = iapp
    app.m_sscontroller = SSController(app.m_db)
    app.m_events.on('beforeRegisterApi', register_routes)

from flask import request, jsonify, session

from sqlalchemy.sql import func

def availiable_port(db) -> int:
    port = db.session.query(func.max(Account.port)).scalar()

    if port is None:
        port = WebguiSetting.getSetting(key='shadowsock_port_range_start',\
            default_value=45001, default_type="Number").getTypedValue()
        db.session.commit()
    else:
        port += 1
    return port

from datetime import datetime, timedelta
def register_routes(api):
    """register rotues for sscontroller
    """
        
    @api.route_admin('/user/getDetail', methods=['GET', 'POST'])
    def admin_getUserDetail():
        userId = request.form.get('userId')
        user = User.query.filter_by(id=userId).first()
        state = {'status': 'success'}
        if not user:
            state['status'] = 'fail'
            return jsonify(state)
        state['user'] = user.to_dict()
        account = Account.query.filter_by(userId=userId).first()
        if not account:
            state['account'] = {}
            return jsonify(state)
        state['account'] = account.to_dict()
        accFlow = AccountFlow.query.filter_by(port=account.port).first()
        state['accountFlow'] = accFlow.to_dict()
        return jsonify(state)


    @api.route_admin('/account/getDetail', methods=['POST'])
    def get_admin_accountDetail():
        id = request.form.get('id', None)
        state = {'status': 'success'}
        if id is None:
            state['status'] = 'fail'
            return jsonify(state)
        acc = Account.query.filter_by(id=id).first()
        state['account'] = acc.to_dict()
        accFlow = AccountFlow.query.filter_by(port=acc.port).first()
        state['accountFlow'] = accFlow.to_dict()
        if acc.userId:
            user = User.query.filter_by(id=acc.userId).first()
            state['user'] = user.to_dict()
        else:
            state['user'] = {}
        
        address = "{}:{}@{}:{}".format(acc.method, acc.password, acc.server, acc.port)
        state['ssAddress'] = address
        return jsonify(state)

    @api.route_admin('/account_port', methods=['POST'])
    def on_get_account_port():
        port = availiable_port(app.m_db)
        return str(port)

    @api.route_admin('/account/get', methods=['POST'])
    def get_admin_account():
        accounts = app.m_sscontroller.list_account()
        # accounts = Account.query.filter().all()
        return jsonify({
            'status': 'success',
            'accounts': [a.to_dict() for a in accounts]
        })

    @api.route_admin('/accountAdd', methods=['POST'])
    def add_account():
        port = request.form.get('port')
        try:
            port = int(port)
        except Exception:
            port = availiable_port(app.m_db)  # should get a useable port

        password = request.form.get('password')

        flow = request.form.get('flow')  # in the unit GB
        try:
            flow = int(flow)
        except:
            flow = 10
        flow = convertFlowToByte(flow, 'G')  # in the unit byte

        duration = request.form.get('duration')
        try:
            duration = int(duration)
        except Exception:
            duration = 7
        if not port or not password or not flow or not duration:
            return 'Bad request'
        expire = timedelta(days=duration) + datetime.now()
        app.m_sscontroller.add_account(port=port, password=password, flow=flow, expire=expire)
        logger.info('successfully add account %d' % port)
        return 'success'
    
    @api.route_admin('/account/updatePassword', methods=['POST'])
    def on_account_update_password():
        newpasswd = request.form.get('password', None)
        port = request.form.get('port', None)
        if newpasswd is None or port is None:
            return jsonify('fail')
        port = int(port)
        if app.m_sscontroller.update_password_by_port(newpasswd, port):
            return jsonify('success')
        else:
            return jsonify('fail')


    @api.route_admin('/account/updateTotalFlow', methods=['POST'])
    def on_account_update_totalflow():
        port = request.form.get('port', None)
        flow = request.form.get('flow', None)  # here the flow is in unit of Gb
        unit = request.form.get('flowUnit', 1024 * 1024 * 1024)
        try:
            port = int(port)
            flow = int(flow)
            unit = int(unit)
        except Exception:
            return jsonify('fail')
        account = Account.query.filter_by(port=port).first()
        if account is None:
            return jsonify('fail')

        flow = flow * unit
        account.totalFlow = flow
        
        app.m_db.session.commit()
        return jsonify('success')


    @api.route_admin('/account/randomPassword', methods=['POST'])
    def on_account_random_password():
        port = request.form.get('port', None)
        result = {'status': 'fail'}
        if port is None:
            return jsonify(result)
        port = int(port)
        newpasswd = getRandomCode(8)
        if app.m_sscontroller.update_password_by_port(newpasswd, port):
            result['status'] = 'success'
            result['password'] = newpasswd
        else:
            result['status'] = 'fail'
        return jsonify(result)

    DAY_SENCONDS = 86400
    @api.route_admin('/account/updateExpiration', methods=['POST'])
    def on_account_update_expiration():
        result = {'status': 'fail'}
        port = request.form.get('port', None)
        days = request.form.get('days', None)
        try:
            port = int(port)
            days = int(days)
        except Exception:
            return jsonify(result)
        result['status'] = 'success'
        # acc = Account.query.filter_by(port=port).first()
        acc = app.m_sscontroller.get_account_by_port(port)
        if not acc:
            result['status'] = 'fail'
            return jsonify(result)
        seconds = days * DAY_SENCONDS
        added = app.m_sscontroller.update_validity(acc, seconds)
        user = User.query.filter_by(id = acc.userId).first()
        if added:
            if user is not None:
                user.type = UserType.ACTIVE.value
            if acc.totalFlow == 0:
                setting = WebguiSetting.getSetting("default_account_flow",\
                    default_value=1, default_type="Number")
                acc.totalFlow = setting.getTypedValue() * 1024 * 1024 * 1024
        else:
            if user is not None:
                user.type = UserType.INVALID.value
        app.m_db.session.commit()
        result['nexpire'] = acc.expire.timestamp()
        return jsonify(result)
    
    @api.route_user('/accountDetail', methods=['POST'])
    def user_accountDetail():
        uid = session['userid']
        account = Account.query.filter_by(userId=uid).first()
        result = {'status': 'fail'}
        if account is not None:
            accountFlow = AccountFlow.query.filter_by(port=account.port).first()
            account._flow = accountFlow
            server = request.host
            if ":" in server:
                server = server.split(':')[0]
            enabled = (account.status == 'added')
            account.server = account.server or server
            account.last_connected = accountFlow.updateTime

            # 用于生成二维码的地址
            # address = '-'.join(
            #     [account.server,
            #     str(account.port), account.password])
            address = "{}:{}@{}:{}".format(account.method, account.password, account.server, account.port)

            result['account'] = account.to_dict()
            result['ssAddress'] = address
            result['enabled'] = enabled
            result['status'] = 'success'
        return jsonify(result)


    @api.route_user('/account/updatePassword', methods=['POST'])
    def on_user_update_account_password():
        password = request.form.get('password')
        if not password:
            return jsonify('failed')
        uid = session['userid']
        return jsonify('success') if app.m_sscontroller.update_password_by_uid(password, uid) else jsonify('fail')
    
    logger.info("Api Registered.")
