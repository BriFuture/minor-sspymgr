# -*- coding: utf-8 -*-
from sspymgr import getRandomCode, convertFlowToByte
from sspymgr.sscontroller import *
import logging
logger = logging.getLogger("plugin_sscontroller")


from datetime import datetime, timedelta
from flask import request, jsonify, session

from sqlalchemy.sql import func

from .flow_stats import FlowRecord5Min, FlowRecordDay

def registerRoutes(api, app):
    """register more rotues for sscontroller
    """
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

    logger.info("routes api registered")

