import os
import sys

pro_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pro_path)

from api import AppApis, BasicApiTestCase


class HomeApis(AppApis):
    def login(self, email, password):
        return self.fetchPost('/home/signin',
            dict(email=email, password=password))

    def logout(self):
        return self.fetchPost('/user/signout')

    def isSignedIn(self):
        return self.fetchPost('/home/isSignedIn')

    def checkcode(self, email=None):
        return self.fetchPost('/home/checkcode', dict(email=email))

    def signup(self, email, password, checkcode):
        return self.fetchPost(
            '/home/signup',
            dict(email=email, password=password, checkcode=checkcode))

    def resetPassword(self):
        pass

    def updatePassword(self, oldPassword, newPassword):
        return self.fetchPost(
            '/user/updatePassword',
            dict(oldPassword=oldPassword, newPassword=newPassword))


import unittest


class HomeTestCase(BasicApiTestCase):
    @classmethod
    def setUpClass(cls):
        cls._init(cls)
        cls.api = HomeApis(cls.app)

    def setUp(self):
        # login as admin
        with self.app.session_transaction() as ses:
            ses['userid'] = 1

    def tearDown(self):
        # print('------last test over-------')
        self.logout()

    def test_signin_signout(self):
        self.logout()
        rv = self.api.login('jw@zbrifuture.cn', 'test')
        assert rv['status'] == 'success' and rv['level'] == 'user'
        rv = self.api.logout()
        assert rv == 'success'

    def test_error_signin(self):
        rv = self.api.login('jw@zbrifuture.cn', 'test2s')
        assert rv['status'] == 'fail' and len(rv['password']) > 0
        rv = self.api.login('', '')
        assert rv['status'] == 'fail'
        rv = self.api.login('j2@zbrifuture.cn', 'test')
        assert rv['status'] == 'fail' and len(rv['email']) > 0

    def test_isSignedin(self):
        self.logout()
        rv = self.api.isSignedIn()
        assert rv['signedIn'] == False

        rv = self.api.login('jw@zbrifuture.cn', 'test')

        rv = self.api.isSignedIn()
        assert rv['signedIn'] == True

        rv = self.api.logout()

        rv = self.api.isSignedIn()
        assert rv['signedIn'] == False

    def test_checkcode(self):
        rv = self.api.checkcode('jw@zbrifuture.cn')
        assert rv['status'] == 'fail'

        rv = self.api.checkcode('testtest.test')
        assert rv['status'] == 'fail'

        rv = self.api.checkcode()
        assert rv['status'] == 'fail'
        count = 3  # MAX_CHECKCODE_ATTEMPT
        from web_settings import WebguiSetting, db
        setting = WebguiSetting.getSetting('signup_remain_limit')
        oldvalue = setting.value
        setting.value = "3"

        db.session.commit()

        for x in range(count):
            rv = self.api.checkcode('test99@test.test')
            print('checkcode status', rv)
            assert rv['status'] == 'success'
        rv = self.api.checkcode('test99@test.test')
        assert rv['status'] == 'fail'
        with self.app.session_transaction() as ses:
            # print('session: ', ses.get('checkcode_attempt'))
            assert ses.get('checkcode_attempt') == count + 1
            
        setting.value = oldvalue
        db.session.commit()

    def test_signup(self):
        cc = 'FOR-TEST'
        with self.app.session_transaction() as ses:
            ses['usercheckcode'] = cc
        rv = self.api.signup('jw@test.test', '123456', cc)
        print(rv)

    def teset_resetPassword(self):
        pass


    
    def test_userUpdatePassword(self):
        with self.app.session_transaction() as ses:
            ses['userid'] = 2
            ses['user'] = 'jw@zbrifuture.cn'
        oldP = 'test1'
        newP = 'new_test'
        rv = self.api.updatePassword(oldPassword=oldP, newPassword=newP)
        assert rv == 'fail'
        oldP = 'test'
        rv = self.api.updatePassword(oldPassword=oldP, newPassword=newP)
        assert rv == 'success'
        # oldP = 'test'
        rv = self.api.updatePassword(oldPassword=newP, newPassword=oldP)
        assert rv == 'success'

if __name__ == '__main__':
    unittest.main()
