import os
import sys

pro_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pro_path)

from api import AppApis, BasicApiTestCase


class BasicApis(AppApis):
    
    def admin_updateInfo(self, comment=None, utype=None, uid=None):
        userId = uid
        return self.fetchPost(
            '/admin/user/updateInfo',
            dict(comment=comment, utype=utype, userId=userId))

    def admin_getAllUser(self):
        return self.fetchPost('/admin/user/getAll')

    def admin_getAllSettings(self):
        return self.fetchPost('/admin/setting/getAll')

    def admin_getAllEmails(self):
        return self.fetchPost('/admin/email/getAll')

    def admin_getPagedEmails(self, page, per_page):
        return self.fetchPost('/admin/email/getPage',
            dict(page=page, per_page=per_page))


import unittest


class BasicTestCase(BasicApiTestCase):
    @classmethod
    def setUpClass(cls):
        cls._init(cls)
        cls.api = BasicApis(cls.app)
    
    def test_getEmail(self):
        rv = self.api.admin_getAllEmails()
        assert rv['status'] == 'success'
        rv = self.api.admin_getPagedEmails(1, 15)
        assert rv['status'] == 'success'

    def test_adminGetAllSetting(self):
        rv = self.api.admin_getAllSettings()
        assert rv['status'] == 'success'

    def test_adminGetAllUser(self):
        rv = self.api.admin_getAllUser()
        assert rv['status'] == 'success'

    def test_adminUpdateUserInfo(self):
        uid = 2
        comment = "Test_adminUpdateUserInfo"
        utype = "active"
        rv = self.api.admin_updateInfo(comment=comment, utype=utype, uid=uid)
        assert rv == 'success'


if __name__ == '__main__':
    unittest.main()
