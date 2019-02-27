# -*- coding: utf-8 -*-

from sspymgr import DB, createLogger
logger = createLogger("plugin_annoucement", stream=False, logger_prefix="[Plugin announcement]")

from datetime import datetime

class Announcement(DB.Model):
    """公告数据模型
    """
    __tablename__ = 'announcement'
    id = DB.Column(DB.Integer, primary_key = True)
    title = DB.Column(DB.String(255), nullable=False)
    variant = DB.Column(DB.String(32)) # primary, success, warn
    content = DB.Column(DB.BLOB)
    createtime = DB.Column(DB.DateTime, default=datetime.now)
    top = DB.Column(DB.Integer, default=0) 

    def to_dict(self):
        content = self.content.decode('utf-8') if self.content is not None else ''
        di = {
            'id': self.id,
            'title': self.title,
            'variant': self.variant,
            'content': content,
            'createTime': self.createtime.timestamp(),
            'top': self.top,
        }
        return di

app = None
from flask import request, jsonify
def registerApis(api):
    @api.route_admin('/announcement/create', methods=['POST'])
    def admin_createAnnouncement():
        title = request.form.get('title', None)
        state = {'status': 'success'}
        if title is None:
            state['status'] = 'fail'
            return jsonify(state)
        variant = request.form.get('variant')
        content = request.form.get('content')
        top = request.form.get('top', 0)
        ann = Announcement(title=title, 
            variant=variant, content=content.encode(), top=top)
        app.m_db.session.add(ann)
        app.m_db.session.commit()
        return jsonify(state)

    @api.route_admin('/announcement/getAll', methods=['GET', 'POST'])
    def admin_getAllAnnouncement():
        anns = Announcement.query.all()
        state = {'status': 'success'}
        state['announcements'] = [a.to_dict() for a in anns]
        return jsonify(state)
    
    @api.route_admin('/announcement/delete', methods=['POST'])
    def admin_delAnnouncement():
        id = request.form.get("id", -1)
        state = {'status': 'success'}
        try:
            id = int(id)
            ann = Announcement.query.filter_by(id=id).delete()
        except Exception as exc:
            state['status'] = 'fail'
            state['desc'] = 'Wrong Id or no such item'
            logger.warn('Invalid operation, {}'.format(exc))
            
        return jsonify(state)

    @api.route_user('/announcement/getAll', methods=['GET', 'POST'])
    def user_getAllAnnouncement():
        anns = Announcement.query.all()
        state = {'status': 'success'}
        state['announcements'] = [a.to_dict() for a in anns]
        return jsonify(state)

    logger.debug("api registered")

def init(iapp):
    global app
    app = iapp
    app.m_events.on("beforeRegisterApi", registerApis)
    logger.info("inited")