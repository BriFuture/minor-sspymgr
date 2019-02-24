# -*- coding: utf-8 -*-
from sspymgr import getRandomCode, convertFlowToByte
from sspymgr.models import db
from sspymgr.sscontroller import *
from sspymgr.globalvars import controller
import logging
logger = logging.getLogger("plugin_sscontroller")


from datetime import datetime, timedelta
from flask import request, jsonify, session

from web_user import User, UserType
from sqlalchemy.sql import func

from .flow_stats import FlowRecord5Min, FlowRecordDay

from web_settings import WebguiSetting
def availiable_port() -> int:
    port = db.session.query(func.max(Account.port)).scalar()
    # db.session.query(db.func.max(User.numLogins)).scalar()
    # maxsql = 'SELECT max(port) FROM %s' % Account.__tablename__
    # max = db.engine.execute( text( maxsql ) ).first()
    # if max[0] is None:
    if port is None:
        port = WebguiSetting.getSetting(key='shadowsock_port_range_start',\
            default_value=45000, default_type="Number").getTypedValue()
        db.session.commit()
    else:
        port += 1
    return port


def registerApi(api):
    """注册路由
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
        port = availiable_port()
        return str(port)

    @api.route_admin('/account/get', methods=['POST'])
    def get_admin_account():
        accounts = controller.list_account()
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
            port = availiable_port()  # should get a useable port

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
        controller.add_account(port=port, password=password, flow=flow, expire=expire)
        logger.info('successfully add account %d' % port)
        return 'success'
    
    @api.route_admin('/account/updatePassword', methods=['POST'])
    def on_account_update_password():
        newpasswd = request.form.get('password', None)
        port = request.form.get('port', None)
        if newpasswd is None or port is None:
            return jsonify('fail')
        port = int(port)
        if controller.update_password(newpasswd, port=port):
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
        
        db.session.commit()
        return jsonify('success')


    @api.route_admin('/account/randomPassword', methods=['POST'])
    def on_account_random_password():
        port = request.form.get('port', None)
        result = {'status': 'fail'}
        if port is None:
            return jsonify(result)
        port = int(port)
        newpasswd = getRandomCode(8)
        if controller.update_password(newpasswd, port=port):
            result['status'] = 'success'
            result['password'] = newpasswd
        else:
            result['status'] = 'fail'
        return jsonify(result)


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
        acc = Account.query.filter_by(port=port).first()
        if not acc:
            result['status'] = 'fail'
            return jsonify(result)
        td = timedelta(days=days)
        acc.expire += td
        if acc.expire > datetime.now():
            user = User.query.filter_by(id = acc.userId).first()
            if user is not None:
                user.type = UserType.ACTIVE.value
            if acc.totalFlow == 0:
                setting = WebguiSetting.getSetting("default_account_flow",\
                    default_value=1, default_type="Number")
                acc.totalFlow = setting.getTypedValue() * 1024 * 1024 * 1024
            
        db.session.commit()
        result['nexpire'] = acc.expire.timestamp()
        return jsonify(result)

    @api.route_admin('/flowUsage/getInDay', methods=['GET', 'POST'])
    def admin_getFlowUsage_day():
        state = {'status': 'success'}
        accountId = request.form.get('accountId', -1)
        account = Account.query.filter_by(id = accountId).first()
        if account is None:
            state['status'] = 'fail'
            return jsonify(state)
        port = account.port
        date = request.form.get('date', None)
        try:
            date = date.split('-')
            y = int(date[0])
            m = int(date[1])
            d = int(date[2])
            now = datetime(year=y, month=m, day=d)
        except:
            now = datetime.now()
        date = '{:%Y-%m-%d}'.format(now)
        records = FlowRecord5Min.query.filter_by(port=port, date=date)
        state['port'] = port
        state['date'] = now.timestamp()
        state['records'] = [fr.to_dict() for fr in records]
        return jsonify(state)
        
    @api.route_admin('/flowUsage/getInMon', methods=['GET', 'POST'])
    def admin_getFlowUsage_month():
        state = {'status': 'success'}
        accountId = request.form.get('accountId', -1)
        account = Account.query.filter_by(id = accountId).first()
        if account is None:
            state['status'] = 'fail'
            return jsonify(state)
        port = account.port
        date = request.form.get('date', None)
        try:
            date = date.split('-')
            y = int(date[0])
            m = int(date[1])
            now = datetime(year=y, month=m)
        except:
            now = datetime.now()
        date = '{:%Y-%m}'.format(now)
        records = FlowRecordDay.query.filter_by(port=port, date=date)
        state['port'] = port
        state['date'] = now.timestamp()
        state['records'] = [fr.to_dict() for fr in records]
        return jsonify(state)

    @api.route_admin('/account/<id>/flowRecord_5min', methods=['GET', 'POST'])
    def get_account_flowRecord_5min(id):
        """ flow unit is KB
        """
        acc = Account.query.filter_by(id=id).first()
        if not acc:
            return '{}'

        now = datetime.now()
        date = '{:%Y-%m-%d}'.format(now)
        records = FlowRecord5Min.query.filter_by(port=acc.port, date=date).all()
        result = {}
        for r in records:
            key = r.hour * 60 + r.minute
            result[key] = r.flow / 1000
        return jsonify(result)

    @api.route_user('/flowUsage/getInDay', methods=['GET', 'POST'])
    def user_getFlowUsage_day():
        state = {'status': 'success'}
        uid = session.get('userid')
        account = Account.query.filter_by(userId=uid).first()
        if account is None:
            state['status'] = 'fail'
            return jsonify(state)
        port = account.port
        date = request.form.get('date', None)
        try:
            date = date.split('-')
            y = int(date[0])
            m = int(date[1])
            d = int(date[2])
            now = datetime(year=y, month=m, day=d)
        except:
            now = datetime.now()
        date = '{:%Y-%m-%d}'.format(now)
        records = FlowRecord5Min.query.filter_by(port=port, date=date)
        state['port'] = port
        state['date'] = now.timestamp()
        state['records'] = [fr.to_dict() for fr in records]
        return jsonify(state)
        
    @api.route_user('/flowUsage/getInMon', methods=['GET', 'POST'])
    def user_getFlowUsage_month():
        state = {'status': 'success'}
        uid = session.get('userid')
        account = Account.query.filter_by(userId=uid).first()
        if account is None:
            state['status'] = 'fail'
            return jsonify(state)
        port = account.port
        date = request.form.get('date', None)
        try:
            date = date.split('-')
            y = int(date[0])
            m = int(date[1])
            now = datetime(year=y, month=m)
        except:
            now = datetime.now()
        date = '{:%Y-%m}'.format(now)
        records = FlowRecordDay.query.filter_by(port=port, date=date)
        state['port'] = port
        state['date'] = now.timestamp()
        state['records'] = [fr.to_dict() for fr in records]
        return jsonify(state)

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
        return 'success' if controller.update_password(password, uid=uid) else 'fail'

    logger.info("routes api registered")

