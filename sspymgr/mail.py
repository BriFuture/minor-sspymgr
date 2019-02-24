# -*- coding: utf-8 -*-

from .models import db
from datetime import datetime

class Email( db.Model ):
    __tablename__ = 'email'
    id = db.Column( db.Integer, primary_key = True, autoincrement = True )
    to = db.Column( db.String( 255 ), nullable=False )
    content = db.Column( db.Text )
    time = db.Column( db.DateTime, default=datetime.now )
    subject = db.Column( db.String( 255 ) )
    ip = db.Column( db.String( 255 ) )
    type = db.Column( db.String( 255 ) )
    remark = db.Column( db.String( 255 ) )
    session = db.Column( db.String( 255 ) )

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
logger = createLogger('email')

class EmailManager(object):
    def __init__(self, config, *args, **kwargs):
        # self.config = config
        _email = config.email
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

        self._sendQueue = Queue()

    def add_email(self, to, subject = None, content = None, type = None ):
        email = Email(
            to=to,
            subject=subject,
            content=content,
            type=type,
            remark="pending")
        db.session.add(email)
        self._sendQueue.put(email)
    
    def send(self, email):
        self._sendQueue.put(email)

    def checkRemain(self):

        if self._sendQueue.empty():
            return
        email = self._sendQueue.get()
        db.session.add(email)
        if self._test:
            email.remark = "debugNotSend"
            logger.debug("[Email] Email generated but not send: {}".format(email))
        else:
            ms = MailSender(self._host, self._account, self._password, self._port)
            ms.send(email)
            email.remark = "sent"
        
        db.session.commit()

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
        