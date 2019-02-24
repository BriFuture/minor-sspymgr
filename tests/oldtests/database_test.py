from os import path
import sys

CURRENT_PATH = path.dirname( path.abspath( __file__ ) )
TOP_PATH = path.abspath( path.join( CURRENT_PATH, path.pardir ) )
WEB_SERVER_PATH = path.abspath( path.join( TOP_PATH, 'webserver' ) )

sys.path.append( TOP_PATH )

from webserver import manager_models as mm

# mm.initAllModels()
import os.path as path
def initAllModels():
    exist = path.exists( mm.SQLITE_DATABASE_LOC )
    if not exist:
        db.create_all()