import json
import unittest
import sys
import os
pro_path = os.path.dirname(os.path.abspath(__file__))
pro_path = os.path.join(pro_path, os.pardir, os.pardir)
sys.path.insert(0, pro_path)
import unittest

class AppApis(object):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        return super().__init__(*args, **kwargs)
    
    def fetchPost(self, url, params=None):
        url = '/api{}'.format(url)
        result = self.app.post(url, data=params).data
        return json.loads(result.decode())
    
    def fetchGet(self, url, params=None):
        url = '/api{}'.format(url)
        result = self.app.get(url, data=params).data
        return json.loads(result.decode())
        
class BasicApiTestCase(unittest.TestCase):

    def _init(self):
        from sspymgr import webgui
        app = webgui.init_all()
        webgui.config.debug = True
        app.config['TESTING'] = True
        client = app.test_client()
        self.app = client

    def logout(self):
        with self.app.session_transaction() as sess:
            if 'userid' in sess:
                sess.pop('userid')
            if 'user' in sess:
                sess.pop('user')