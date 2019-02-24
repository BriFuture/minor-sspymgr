import os
import unittest
import tempfile
# import sspymgr
import json

from sspymgr import  sscontroller

class SSControllerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def tearDown(self):
        print('------last test over-------')

    def test_signin_signout(self):
        rv = self.api.login('jw@zbrifuture.cn', 'test')
        assert rv['status'] == 'success' and rv['level'] == 'user'
        rv = self.api.logout()
        assert rv == 'success'

if __name__ == '__main__':
    unittest.main()
