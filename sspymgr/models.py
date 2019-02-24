# -*- coding: utf-8 -*-
from .path_helper import DATA_DIR
from os.path import abspath, join

_SQLITE_DATABASE = 'database.db'
SQLITE_DATABASE_LOC = abspath( join( DATA_DIR, _SQLITE_DATABASE ) )

"""
from ..globalvars import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % SQLITE_DATABASE_LOC
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy( app )
"""


### for pagenate

from sqlalchemy.orm import  Query
import math

def paginate(self, page=None, per_page=None, to_dict=True):
    """
    分页函数
    :param self:
    :param page:
    :param per_page:
    :return:
    """
    if page is None:
        page = 1

    if per_page is None:
        per_page = 20

    items = self.limit(per_page).offset((page - 1) * per_page).all()

    if not items and page != 1:
        return {'total': 0, 'page': page, 'error': 'no such items'}
        
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = self.order_by(None).count()
    
    if to_dict:
        ditems = [item.to_dict() for item in items]
    else:
        ditems = items

    return {
        'page': page, 
        'per_page': per_page, 
        'total': total, 
        'items': ditems
    }
    # return Pagination(self, page, per_page, total, items)


from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sqlalchemy

def createDatabase():
    Model = declarative_base()

    engine = sqlalchemy.create_engine('sqlite:///{}'.format(SQLITE_DATABASE_LOC))
    Model.metadata.bind = engine
    session = orm.scoped_session(orm.sessionmaker(bind = engine))

    sqlalchemy.session = session
    sqlalchemy.Model = Model
    sqlalchemy.engine = engine

    sqlalchemy.create_all = Model.metadata.create_all
    Query.paginate = paginate
    Model.query = session.query_property()
    return sqlalchemy

db = createDatabase()
