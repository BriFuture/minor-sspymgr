# -*- coding: utf-8 -*-
from sspymgr import DB, \
    createLogger, getRandomCode, formatTime

logger = createLogger("plugin_order", stream=False, logger_prefix="[Plugin Order]")
requirement = ['web_user']

from datetime import datetime, timedelta
from sqlalchemy.sql import text


class Product(DB.Model):
    __tablename__ = 'product'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    # name = DB.Column( DB.String( 255 ) )
    type = DB.Column(DB.Integer)  # 0 or none stands by enabled
    flow = DB.Column(DB.Integer)  # unit: Mn
    price = DB.Column(DB.Float)  # unit: ￥
    enable = DB.Column(DB.Boolean, default=True)
    duration = DB.Column(DB.Integer)  # unit: seconds
    buffer_period = DB.Column(DB.Integer)  # unit: seconds

    @staticmethod
    def add_type(price: float, flow: int, duration: timedelta,
                 buffer_period: timedelta):
        dseconds = duration.total_seconds()
        bseconds = buffer_period.total_seconds()
        ot = Product(
            price=price, flow=flow, duration=dseconds, buffer_period=bseconds)
        return ot

    def to_dict(self):
        return {
            "id": self.id,
            "flow": self.flow,
            "price": self.price,
            "enable": self.enable,
            "duration": self.duration,
            "bufferPeriod": self.buffer_period
        }

    def to_dict(self):
        di = {
            "id": self.id,
            "flow": self.flow,
            "price": self.price,
            "enable": self.enable,
            "duration": self.duration,
            "bufferPeriod": self.buffer_period
        }
        return di

    def __repr__(self):
        return '<Product %d %s>' % (self.id, self.enable)

class ProductQrcode(DB.Model):
    __tablename__ = 'productQrcode'
    id = DB.Column(DB.Integer, primary_key=True)
    pid = DB.Column(DB.Integer, nullable=False)  # product Id
    category = DB.Column(DB.String(32), nullable=True) # such as alipay or wechatpay
    qrcode = DB.Column(DB.TEXT)  # base64 encoded image
    desc = DB.Column(DB.String(255))  
    path = DB.Column(DB.String(255)) # if save image as files, path to find it
    remark = DB.Column(DB.String(32)) # reserved

    def to_dict(self):
        di = {
            "id": self.id,
            "pid": self.pid,
            "category": self.category,
            "qrcode": self.qrcode,
            "desc": self.desc,
            "path": self.path,
            "remark": self.remark,      
        }
        return di


class Order(DB.Model):
    __tablename__ = 'order'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    uid = DB.Column(DB.Integer, nullable=False)
    pid = DB.Column(DB.Integer, nullable=False)
    server = DB.Column(DB.String(255))
    code = DB.Column(DB.String(32))
    alipay = DB.Column(DB.Float)
    wechatpay = DB.Column(DB.Float)
    orderTime = DB.Column(DB.DateTime)
    commentByUser = DB.Column(DB.Text, default='')
    # whether the Manager has confirmed this order
    checked = DB.Column(DB.Boolean, default=False)  
    # buffer period
    bufferPeriodExpire = DB.Column(DB.DateTime)  
    expire = DB.Column(DB.DateTime)

    @staticmethod
    def place_order(uid: int, product: Product, **kwargs):
        od = Order(uid=uid, pid=product.id)
        # od.code = getRandomCode( 32 )
        od.code = '{:%Y%m%d%H%M%S}{:1}'.format(datetime.now(),
                                               getRandomCode(18))
        od.commentByUser = kwargs.get('comment', '')
        now = datetime.now()
        od.orderTime = now
        od.checked = kwargs.get('checked', False)
        od.bufferPeriodExpire = timedelta(seconds=product.buffer_period) + now
        od.expire = timedelta(seconds=product.duration) + now
        app.m_db.session.add(od)
        app.m_db.session.commit()
        # return od


    def is_valid(self):
        now = datetime.now()
        if not self.checked:
            return now < self.bufferPeriodExpire
        return now < self.expire

    def check_it(self, alipay=0, wechatpay=0):
        # if not alipay
        self.checked = True
        self.alipay = alipay
        self.wechatpay = wechatpay

    def relateProduct(self):
        return Product.query.filter_by(id=self.productId).first()

    def to_dict(self):
        di = {
            'id': self.id,
            'uid': self.uid,
            'pid': self.pid,
            'server': self.server,
            'code': self.code,
            'alipay': self.alipay,
            'wechatpay': self.wechatpay,
            'orderTime': self.orderTime.timestamp(),
            'commentByUser': self.commentByUser,
            'checked': self.checked,
            'bufferPeriodExpire': self.bufferPeriodExpire.timestamp(),
            'expire': self.expire.timestamp(),
        }
        return di


def init_product_type():
    sql = 'SELECT count(*) FROM %s' % Product.__tablename__
    res = app.m_db.engine.execute(text(sql)).first()
    
    count = res[0]
    if count == 0:
        ptype = (
            (1,  8 * 1024, timedelta(days=7), timedelta(hours=4)), 
            (2, 18 * 1024, timedelta(days=15), timedelta(hours=8)),
            (2.5, 24 * 1024, timedelta(days=15), timedelta(hours=10)), 
            (4, 40 * 1024, timedelta(days=30), timedelta(days=1)),
            (5, 55 * 1024, timedelta(days=30), timedelta(days=1))
        )
        for ot in ptype:
            new_product = Product.add_type(ot[0], ot[1], ot[2], ot[3])
            app.m_db.session.add(new_product)
        app.m_db.session.commit()


from flask import jsonify, session, request
app = None

def user_confirm_order(user):
    """用户成功下单时通知管理员
    """
    from web_user import getSuperManager
    admin = getSuperManager()
    content = "用户(id: {}, email: {}) 于 {} 成功下单，请确认。".format(
        user.id, user.email, datetime.now())

    app.m_emailManager.add_email(
        to=admin.email,
        subject="用户下单",
        content=content,
        type="user confirm order")

from sspymgr.sscontroller import Account, AccountFlow

def registerApi(api):
    from web_user import User, UserType, getSuperManager
    @api.route_admin('/product/getAll', methods=['POST'])
    def get_admin_products():
        prodcuts = Product.query.all()
        return jsonify({
            'status': 'success',
            'products': [p.to_dict() for p in prodcuts]
        })

    @api.route_admin('/product/get', methods=['GET', 'POST'])
    def admin_getProduct():
        id = request.form.get('id', -1)
        product = Product.query.filter_by(id=id).first()
        if product is None:
            return jsonify({'status': 'fail'})

        qrcodes = ProductQrcode.query.filter_by(pid=id).all()

        return jsonify({
            'status': 'success',
            'product': product.to_dict(),
            'qrcodes': [qr.to_dict() for qr in qrcodes],
        })

    @api.route_admin('/product/update', methods=['POST'])
    def admin_updateProduct():
        """更新或添加 Product
        """
        id = request.form.get('id', None)
        oldOne = Product.query.filter_by(id = id).first()
        if oldOne is None:
            oldOne = Product(price=5, duration=1296000,buffer_period=86400, flow=40960)
            app.m_db.session.add(oldOne)
            # return jsonify( {'status': 'fail'})
        oldOne.price = request.form.get('price', oldOne.price)
        oldOne.duration = request.form.get('duration', oldOne.duration)
        oldOne.flow = request.form.get('flow', oldOne.flow)
        oldOne.buffer_period = request.form.get('bufferPeriod', oldOne.buffer_period)
        # oldOne.enable = request.form.get('enable', oldOne.enable)
        enable = request.form.get('enable', None)
        if enable is not None:
            oldOne.enable = (enable == 'true')
        app.m_db.session.commit()
        return jsonify({'status': 'success'})

    @api.route_admin('/productQrcode/update', methods=['POST'])
    def admin_updateProductQrcode():
        # print(request.form)
        id = request.form.get('id')
        qrcode = ProductQrcode.query.filter_by(id=id).first()
        if qrcode is None:
            pid = request.form.get('productId', -1)
            if pid == -1:
                return jsonify({'status': 'fail'})
            qrcode = ProductQrcode(pid = pid, category='alipay')
            app.m_db.session.add(qrcode)
        qrcode.category = request.form.get('category', qrcode.category)
        qrcode.qrcode = request.form.get('qrcode')
        qrcode.desc = request.form.get('desc', qrcode.desc)
        qrcode.path = request.form.get('path', qrcode.path)
        qrcode.remark = request.form.get('remark', qrcode.remark)
        
        app.m_db.session.commit()
        return jsonify({'status': 'success'})

    @api.route_admin('/productQrcode/delete', methods=['POST'])
    def admin_deleteProductQrcode():
        id = request.form.get('id', -1)
        if id == -1:
            return jsonify({'status': 'fail'})
        qrcode = ProductQrcode.query.filter_by(id=id).delete()
        return jsonify({'status': 'success'})

    @api.route_admin('/orderHistory/get', methods=['POST'])
    def get_admin_order():
        page, per_page = api.getPageArgs()
        
        orders = Order.query.paginate(page=page, per_page=per_page)

        return jsonify({
            'status': 'success',
            'orders': orders
        })
    
    @api.route_admin('/orderHistory/getAll', methods=['GET', 'POST'])
    def admin_getAllOrderHistory():
        orders = Order.query.all()

        return jsonify({
            'status': 'success',
            'orders': [o.to_dict() for o in orders]
        })

    @api.route_user('/product/canPlace', methods=['GET', 'POST'])
    def can_user_place_order():
        """check whether user is able to place order
        """
        uid = session.get('userid')
        result = {'status': 'success'}
        account = Account.query.filter_by(userId=uid).first()
        if account is None:
            result['status'] = 'fail'
            result['canPlaceOrder'] = False
            return result
        now = datetime.now()
        next_time = account.expire - timedelta(days=1)
        if next_time > now:
            result['canPlaceOrder'] = False
            result['expire'] = formatTime(account.expire)
            result['nextPlaceOrderTime'] = formatTime(next_time)
        else:
            result['canPlaceOrder'] = True

        return jsonify(result)

    @api.route_user('/product/getAll', methods=['GET', 'POST'])
    def user_getAllProducts():
        """返回所有可用的 producte
        """
        products = Product.query.all()
        np = []
        for product in products:
            if product.enable:
                p = product.to_dict()
                p['alipay'] = ProductQrcode.query.filter_by(pid=product.id, category='alipay').count() > 0
                p['wechatpay'] = ProductQrcode.query.filter_by(pid=product.id, category='wechatpay').count() > 0
                np.append(p)

        return jsonify(np)

    @api.route_user('/product/getDetail', methods=['GET', 'POST'])
    def user_getProductDetail():
        """获取产品的详细信息
        """
        pid = request.form.get('product', -1)
        state = {'status': 'success'}
        product = Product.query.filter_by(id=pid).first()
        if pid == -1 or product is None:
            state['status'] = 'fail'
            return jsonify(state)

        p = product.to_dict()
        state['product'] = p
        qrcodes = ProductQrcode.query.filter_by(pid=pid).all()
        state['qrcodes'] = [qr.to_dict() for qr in qrcodes]
        return jsonify(state)

    @api.route_user('/product/confirm', methods=['POST'])
    def user_confirmOrder():
        """用户点击确认下单后的操作
        """
        state = {'status': 'success'}
        pid = request.form.get('product', -1)
        product = Product.query.filter_by(id=pid).first()
        if product is None:
            state['status'] = 'fail'
            return jsonify(state)

        comment = request.form.get('comment', '')
        uid = session['userid']
        flow = product.flow * 1024 * 1024  # product flow is stored in unit mb, convert it in byte

        # order history
        Order.place_order(uid, product, comment=comment)

        if app.m_sscontroller.renew_account(
                flow, timedelta(seconds=product.duration), uid=uid):
            user = User.query.filter_by(id=uid).first()
            user.type = UserType.ACTIVE.value
            user_confirm_order(user)
            app.m_db.session.commit()
        else:
            state['status'] = 'fail'
        return jsonify(state)

    @api.route_user('/orderHistory/get', methods=['GET', 'POST'])
    def user_getOrderHistory():
        uid = session.get('userid')
        orders = Order.query.filter_by(uid=uid).all()
        order = [o.to_dict() for o in orders]
        return jsonify(order)

    logger.debug("api Registered")

from sspymgr import Manager
def init(iapp: Manager):
    global app
    app = iapp
    app.m_events.on('beforeRegisterApi', registerApi)
    init_product_type()
    logger.debug("inited")