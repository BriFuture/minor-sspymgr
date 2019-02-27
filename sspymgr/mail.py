# -*- coding: utf-8 -*-

from .models import DB
from datetime import datetime

class Email( DB.Model ):
    __tablename__ = 'email'
    id = DB.Column( DB.Integer, primary_key = True, autoincrement = True )
    to = DB.Column( DB.String( 255 ), nullable=False )
    content = DB.Column( DB.Text )
    time = DB.Column( DB.DateTime, default=datetime.now )
    subject = DB.Column( DB.String( 255 ) )
    ip = DB.Column( DB.String( 255 ) )
    type = DB.Column( DB.String( 255 ) )
    remark = DB.Column( DB.String( 255 ) )
    session = DB.Column( DB.String( 255 ) )

    def to_dict(self):
        di = {
            'id': self.id,
            'to': self.to,
            'content': self.content,
            'time': self.time.timestamp(),
            'subject': self.subject,
            'ip': self.ip,
            'type': self.type,
            'remark': self.remark,
            'session': self.session,            
        }
        return di

    def __repr__(self):
        return "<Email to: {}, subject: {}, content: {}, time: {}>"\
            .format(self.to, self.subject, self.content, self.time)

from queue import Queue
import smtplib
import yaml
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from .path_helper import createLogger
logger = createLogger('email', stream=False)

class EmailManager(object):
    def __init__(self, config, database, *args, **kwargs):
        # self.config = config
        _email = config.email
        self.db = database
        self._test = config.debug
        self._host     = _email[ 'host' ]
        self._account  = _email[ 'account' ]
        self._password = _email[ 'password' ]
        self._port     = _email.get( 'port' ) or 465
        if( self._host == 'smtp host' ):
            logger.warning( '[Email] Please Place Your smtp account into config file')
            import sys
            sys.exit( 1 )
        if( self._host == None ) :
            raise ValueError
        self._process_pending = False
        self._sendQueue = Queue()

    def add_email(self, to, subject = None, content = None, type = None ):
        email = Email(
            to=to,
            subject=subject,
            content=content,
            type=type,
            remark="pending")
        # db.session.add(email)
        self._sendQueue.put(email)
    
    def send(self, email: Email):
        self._sendQueue.put(email)

    def checkRemain(self):
        if self._sendQueue.empty():
            self.checkPending()
            return
        email = self._sendQueue.get()
        self.__send(email, commit=True)

    def checkPending(self):
        if self._process_pending == True:
            return
        self._process_pending = True
        emails = Email.query.filter_by(remark='pending').all()
        for e in emails:
            self.__send(e)
        self.db.session.commit()
        self._process_pending = False

    def __send(self, email: Email, commit = False):
        self.db.session.add(email)
        logger.debug("Geting email and ready to send it")
        if self._test:
            email.remark = "debugNotSend"
            logger.info("Email generated but not send: {}".format(email))
        else:
            ms = MailSender(self._host, self._account, self._password, self._port)
            ms.send(email)
            email.remark = "sent"
            logger.debug("Email generated and send: {}".format(email))
        if commit:
            self.db.session.commit()

class MailSender(object):
    def __init__(self, host, account, password, port, *args, **kwargs):
        self.host = host
        self.account = account
        self.password = password
        self.port = port
        self.server = smtplib.SMTP_SSL(self.host, self.port)
        return super().__init__(*args, **kwargs)
    
    def send(self, email: Email):
        msg = MIMEText(email.content, 'html', 'utf-8')
        msg['Subject'] = Header(email.subject, 'utf-8').encode()
        msg['From'] = self.__format_addr('SSPY-Mgr <{}>'.format(self.account))
        msg['To'] = self.__format_addr('Receiver <{}>'.format(email.to) )
        self.server.connect( self.host, self.port )
        # self.server.starttls()
        self.server.ehlo()
        self.server.login( self.account, self.password)
        self.server.sendmail( self.account, email.to, msg.as_string())
        self.server.quit()

    def __format_addr( self, s ):
        name, addr = parseaddr(s)
        return formataddr( ( Header(name, 'utf-8').encode(), addr ) )


def registerApi(api):
    from flask import jsonify 
    @api.route_admin('/email/getAll', methods=['GET', 'POST'])
    def admin_getAllEmails():
        emails = Email.query.all()
        em = [e.to_dict() for e in emails]
        return jsonify({'status': 'success', 'emails': em})

    @api.route_admin('/email/getPage', methods=['GET', 'POST'])
    def admin_getPageEmails():
        page, per_page = api.getPageArgs()
        emails = Email.query.paginate(page=page, per_page=per_page)
        return jsonify({'status': 'success', 'emails': emails})
    logger.info("Api registered")


def init(app):
    app.m_events.on("beforeRegisterApi", registerApi)
