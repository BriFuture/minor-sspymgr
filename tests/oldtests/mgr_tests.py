import os, unittest, tempfile

import sys
path = os.path
CURRENT_PATH = path.dirname( path.abspath( __file__ ) )
TOP_PATH = path.abspath( path.join( CURRENT_PATH, path.pardir ) )
WEB_SERVER_PATH = path.abspath( path.join( TOP_PATH, 'webserver' ) )

sys.path.append( TOP_PATH )

from webserver import webgui

class MgrTestCase( unittest.TestCase ):

    def setUp( self ):
        self.db_fd, webgui.app.config[ 'DATABASE' ] = tempfile.mkstemp()
        webgui.app.config[ 'TESTING' ] = True
        self.app = webgui.app.test_client()
        webgui.initAllModels()

    def tearDown( self ):
        os.close( self.db_fd )
        os.unlink( webgui.app.config[ 'DATABASE' ] )

    def test_empty_db( self ):
        rv = self.app.get( '/' )
        # print( rv.data )
        assert rv.data is not None

    def login( self, username, password ):
        return self.app.post( '/home/signin', data = dict( 
            username = username, password = password
        ), follow_redirects = True )

    def logout( self ):
        return self.app.get( '/logout', follow_redirects = True )

    def test_login_logout( self ):
        pass

if __name__ == '__main__':
    unittest.main()