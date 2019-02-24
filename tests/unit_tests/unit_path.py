import os, os.path as path, sys

CURRENT_PATH = path.dirname( path.abspath( __file__ ) )
TOP_PATH = path.abspath( path.join( CURRENT_PATH, path.pardir, path.pardir ) )
WEBSER_PATH = path.abspath( path.join( TOP_PATH, 'webserver' ) )

sys.path.append( TOP_PATH )