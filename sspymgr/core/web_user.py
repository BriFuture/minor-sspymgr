# -*- coding: utf-8 -*-

from sspymgr import DB, createLogger
from sspymgr import getRandomCode, convertFlowToByte

from flask import session, request, jsonify
from datetime import datetime, timedelta
import hashlib

logger = createLogger(
    "core_user", stream=False, logger_prefix="[Plugin User]")


class User(DB.Model):
    __tablename__ = 'user'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    type = DB.Column(DB.String(255))
    salt = DB.Column(DB.String(8), nullable=False)
    email = DB.Column(DB.String(255), nullable=False)
    group = DB.Column(DB.Integer, default=0)
    level = DB.Column(DB.Integer, default=1)
    comment = DB.Column(DB.String(255), default='')
    password = DB.Column(DB.String(255), nullable=False)
    telegram = DB.Column(DB.String(255))
    username = DB.Column(DB.String(255))
    lastLogin = DB.Column(DB.DateTime)
    createTime = DB.Column(DB.DateTime)
    resetPasswordId = DB.Column(DB.String(255))
    resetPasswordTime = DB.Column(DB.DateTime)

    Type_Active = "active"
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # self.password = password
        self.salt = getRandomCode(8)
        self.password = self.__gen_passwd(self.password)
        self.createTime = datetime.now()

    def __repr__(self):
        return '<User %s %s %s>' % (self.email, self.salt, self.password)

    def __gen_passwd(self, password):
        """
        Just generate secure password, but not modify object's password attribute,
        parameter password can't be None or self.password, otherwise the method 
        which checks whether password is valid will return a Fake result
        """
        return hashlib.sha256((self.salt + password).encode()).hexdigest()

    def updatePassword(self, new_passwd):
        self.password = self.__gen_passwd(new_passwd)

    def isPasswordValid(self, password):
        """判断用户密码是否正确 
        """
        password = str(password)
        password = self.__gen_passwd(password)
        return password == self.password

    def request_reset_passwd(self):
        self.resetPasswordId = getRandomCode(24)
        self.resetPasswordTime = datetime.now()

    def do_reset_passwd(self, passwdId, new_passwd):
        """reset password and clear requestId
        @returns
            True if succesfully reset, False otherwise
        """
        if not self.resetPasswordId or not self.resetPasswordTime:
            return False
        now = datetime.now()
        diff = now - self.resetPasswordTime

        if diff > timedelta(hours=3):
            # overtime, invalid
            return False

        if passwdId != self.resetPasswordId:
            return False

        self.password = self.__gen_passwd(new_passwd)
        self.resetPasswordId = ''
        return True

    def to_dict(self):
        lastLogin = self.lastLogin.timestamp(
        ) if self.lastLogin is not None else None
        di = {
            'id': self.id,
            'email': self.email,
            'type': self.type,
            'group': self.group,
            'comment': self.comment,
            'telegram': self.telegram,
            'username': self.username,
            'lastLogin': lastLogin,
            'createTime': self.createTime.timestamp(),
        }
        return di


class Group(DB.Model):
    __tablename__ = 'group'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.DateTime)
    order = DB.Column(DB.String(255))
    comment = DB.Column(DB.DateTime)
    showNotice = DB.Column(DB.Integer, default=1)
    multiAccount = DB.Column(DB.Integer, default=0)


from enum import Enum, unique


@unique
class UserType(Enum):
    BANNED = 'banned'
    TRIAL = 'trial'
    ACTIVE = 'active'
    INVALID = 'invalid'
    NOTIFIED = 'notified'
    DEFAULT = 'default'
    TEST = 'test'


# class UserStatus(DB.Model):
#     __tablename__ = 'UserStatus'
#     userId = DB.Column(DB.Integer, nullable=False)
#     webStatus = DB.Column(DB.String(64), default=UserType.DEFAULT.value)
#     ssStatus = DB.Column(DB.String(64))


def getCurrentUser():
    uid = session.get('userid')
    user = User.query.filter_by(id=uid).first()
    return user


def isManager(user=None):
    """If user is set, check if user is manager;
    Else check it by session
    """
    if user is not None:
        return user.id == 1
    if 'userid' in session:
        return session.get('userid', -1) == 1
    return False


def getSuperManager() -> User:
    """Get the super manager.
    """
    return User.query.filter_by(id=1).first()


def _user_signin(user):
    """process user signin action, assume user is validated
    """
    session['user'] = user.email
    session['userid'] = user.id
    user.lastLogin = datetime.now()


def _send_checkcode_email(emailaddr, emailManager):
    """get check code when signup
    """
    rcode = getRandomCode()
    session['usercheckcode'] = rcode
    content = '你好，注册验证码为: %s' % rcode
    emailManager.add_email(
        to=emailaddr,
        subject='SSPY SignUp',
        content=content,
        type="signup checkcode")


def _send_reset_link(host, email, code, emailManager):
    """generate reset password link
    """
    link = host + '/vhome#/resetPassword/' + code
    # url_for( 'home.on_resetPasswdWithId', code = code)
    content = 'Hi, 重置密码的链接为: %s，请在时限内重置你的密码' % link
    emailManager.add_email(
        to=email,
        subject="SSPY Reset Password Link",
        content=content,
        type="reset password")


MAX_CHECKCODE_ATTEMPT = 3
CHECKCODE_TIMEOUT = timedelta(minutes=10)

from sspymgr import isEmailMatched

def registerApi(api, app):
    from . import WebguiSetting

    @api.route('/home/signin', methods=['POST'])
    def on_home_signin():
        """Basic entry to signin for users who want to use sspymgr
        """
        # first of all, validate input data
        resp = {'status': 'success'}
        emailaddr = request.form.get('email', '')
        password = request.form.get('password', '')
        valid = True
        if (len(emailaddr) == 0):
            resp['email'] = 'Email is Empty'
            valid = False
        if (len(password) == 0):
            resp['password'] = 'Password is Empty'
            valid = False

        if valid is False:
            resp['status'] = 'fail'
            return jsonify(resp)
        # find correspoding user and if not found, raise error
        user = User.query.filter_by(email=emailaddr).first()
        if user is None:
            resp['status'] = 'fail'
            resp['email'] = 'Email is not valid'
            return jsonify(resp)

        if user.isPasswordValid(password):
            # able to sign in
            _user_signin(user)
            session.permanent = request.form.get(
                'keep_signedin') == 'remember-me'
            resp['status'] = 'success'
            resp['level'] = 'admin' if isManager(user) else 'user'
        else:
            # unable to signin, password may be wrong
            resp['status'] = 'fail'
            resp['password'] = 'Password is wrong'
        return jsonify(resp)

    @api.route('/home/isSignedIn', methods=['POST'])
    def is_user_signedIn():
        resp = {'signedIn': False, 'level': 'user'}
        if 'userid' in session:
            resp['signedIn'] = True
            if isManager():
                resp['level'] = 'admin'

        return jsonify(resp)

    @api.route('/home/checkcode', methods=['POST'])
    def on_send_checkcode():
        resp = {'status': 'success'}
        email = request.form.get('email', '')
        if len(email) == 0:
            resp['status'] = 'fail'
            resp['desc'] = 'Email is empty'
            return jsonify(resp)

        exists = User.query.filter_by(email=email).count() > 0
        if not isEmailMatched(email) or exists:
            resp['status'] = 'fail'
            resp['desc'] = 'Wrong Email or Email already in use'
            return jsonify(resp)

        if 'checkcode_attempt' not in session:
            session['checkcode_attempt'] = 0
            session['checkcode_start'] = datetime.now().timestamp()

        singup_limit = WebguiSetting.getSetting('signup_remain_limit',\
            default_value=4, default_type="Number").getTypedValue()
        if singup_limit == 0:
            resp['status'] = 'fail'
            resp['desc'] = 'Sorry, no more users can signup.'
            return jsonify(resp)

        session['checkcode_attempt'] += 1

        if session['checkcode_attempt'] <= MAX_CHECKCODE_ATTEMPT:
            _send_checkcode_email(email, app.m_emailManager)
        else:
            start = datetime.fromtimestamp(session['checkcode_start'])
            now = datetime.now()
            if now - start > CHECKCODE_TIMEOUT:
                session['checkcode_attempt'] = 1
                _send_checkcode_email(email, app.m_emailManager)
            else:
                resp['status'] = 'fail'
                resp[
                    'desc'] = 'Please wait a few minutes before resend check code.'
        app.m_db.session.commit()
        return jsonify(resp)

    @api.route('/home/signup', methods=['POST'])
    def on_home_signup():
        resp = {'status': 'fail'}
        valid = True
        if (not 'usercheckcode' in session):
            resp['code'] = 'Get checkcode first.'
            valid = False

        email = request.form.get('email', '')
        checkcode = request.form.get('checkcode', '')
        password = request.form.get('password', '')
        if (len(email) == 0):
            resp['email'] = 'Email is Empty'
            valid = False
        if (len(checkcode) == 0):
            resp['code'] = 'CheckCode is Empty'
            valid = False
        if (len(password) == 0):
            resp['password'] = 'Password is Empty'
            valid = False
        if valid and not isEmailMatched(request.form['email']):
            resp['email'] = 'Wrong email or not able to sign up now'
            valid = False

        if valid is False:
            return jsonify(resp)

        user = User.query.filter_by(email=email).first()
        if user is not None:
            resp['status'] = 'fail'
            resp['email'] = 'Email has already in use'
            return jsonify(resp)

        if (session.get('usercheckcode').lower() == checkcode.lower()):
            email = email.strip()
            user = User(email=email, password=password)
            app.m_db.session.add(user)
            setting = WebguiSetting.getSetting(key='signup_remain_limit')
            setting.value = setting.getTypedValue() - 1
            app.m_db.session.commit()
            # add account into shadowsocks server, but there is a problem is that if not committed,
            # user.id will be None
            user = User.query.filter_by(email=email).first()
            app.m_events.trigger(
                "webuser_signup_success",
                dict(
                    userId=user.id,
                    flow=convertFlowToByte(1, 'G'),
                ))

            # checkcode will be removed after user have been added
            session.pop('usercheckcode')
            # auto signin
            resp['status'] = 'success'
            _user_signin(user)

            app.m_db.session.commit()
        return jsonify(resp)

    @api.route('/home/requestReset', methods=['POST'])
    def on_home_requestReset():
        state = {'status': 'success'}
        email = request.form.get('email', '')
        if (len(email) == 0 or not isEmailMatched(request.form['email'])):
            state['status'] = 'fail'
        user = User.query.filter_by(email=email).first()

        if user:
            user.request_reset_passwd()
            code = '%d_%s' % (user.id, user.resetPasswordId)
            _send_reset_link(request.host, email, code, app.m_emailManager)
            app.m_db.session.commit()
        else:
            state['status'] = 'fail'
        return jsonify(state)

    @api.route('/home/resetPassword', methods=['POST'])
    def on_home_doResetPasswdWithId():
        code = request.form.get('code', '')
        code = code.split('_')
        state = {'status': 'success'}
        if len(code) < 2:
            state['status'] = 'fail'
            state['hint'] = 'Wrong code'
            return jsonify(state)
        userId = code[0]
        resetId = code[1]
        user = User.query.filter_by(id=userId, resetPasswordId=resetId).first()
        newpw = request.form.get('newPassword', '')
        if user is None or len(newpw) == 0:
            state['status'] = 'fail'
            state['hint'] = 'Wrong Password'
            return jsonify(state)

        result = user.do_reset_passwd(resetId, newpw)
        app.m_db.session.commit()
        if not result:
            state['status'] = 'fail'
            state['hint'] = 'Your code seems not right or expired'
        return jsonify(state)

    # =====================  user route =====================
    @api.route_user('/signout', methods=['POST'])
    def user_signout():
        session.pop('user')
        session.pop('userid')
        return jsonify('success')

    @api.route_user('/updatePassword', methods=['POST'])
    def on_user_update_password():
        uid = session.get('userid')
        user = User.query.filter_by(id=uid).first()
        oldp = request.form.get('oldPassword')
        if user is None or not user.isPasswordValid(oldp):
            return jsonify('fail')
        newp = request.form.get('newPassword')
        user.updatePassword(newp)
        app.m_db.session.commit()
        return jsonify('success')

    # ===============  admin route  =================
    @api.route_admin('/user/updateInfo', methods=['POST'])
    def admin_updateUserInfo():
        comment = request.form.get('comment')
        utype = request.form.get('type')
        uid = request.form.get('userId')
        user = User.query.filter_by(id=uid).first()
        if user is None:
            return jsonify('fail')
        user.comment = comment
        user.type = utype
        app.m_db.session.commit()
        return jsonify('success')

    @api.route_admin('/user/getAll', methods=['POST'])
    def get_admin_user():
        users = User.query.filter().all()
        return jsonify({
            'status': 'success',
            'users': [u.to_dict() for u in users]
        })

    logger.info("api registered.")