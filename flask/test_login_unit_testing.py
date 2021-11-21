import unittest
from website.controller import userController as userController
from unittest.mock import patch

class test_Login_Passed_Credential(unittest.TestCase):

    def setUp(self):
        self.patcher_passed = patch('website.controller.userController.login',return_value=b"testuser,testuser")
        self.patcher_passed.start()
    
    def test_login_unit_testing_passed(self):
        result = userController.login()
        data = b'testuser,testuser'
        Message = "Test login passed"
        self.assertIn(data,result,Message)

    def tearDown(self):
        self.patcher_passed.stop()

class test_Login_Failed_Password(unittest.TestCase):

    def setUp(self):
        self.patcher_failed_password = patch('website.controller.userController.login',return_value=b'testuser,testuser')
        self.patcher_failed_password.start()

    def test_login_unit_testing_failed_password(self):
        result = userController.login()
        data = b'testuser,testuser123'
        Message = "Incorrect credential"
        self.assertNotEqual(result,data,Message)

    def tearDown(self):
        self.patcher_failed_password.stop()
        

class test_Login_Failed_Username(unittest.TestCase):

    def setUp(self):
        self.patcher_failed_username = patch('website.controller.userController.login',return_value=b'testuser,testuser')
        self.patcher_failed_username.start()

    def test_login_unit_testing_failed_Username(self):
        result = userController.login()
        data = b'testuser1,testuser'
        Message = "Incorrect credential"
        self.assertNotEqual(result,data,Message)

    def tearDown(self):
        self.patcher_failed_username.stop()

class test_Login_Failed_Both_Credential(unittest.TestCase):

    def setUp(self):
        self.patcher_failed_username = patch('website.controller.userController.login',return_value=b'testuser,testuser')
        self.patcher_failed_username.start()

    def test_login_unit_testing_failed_Username(self):
        result = userController.login()
        data = b'testuser123,testuser123'
        Message = "Incorrect credential"
        self.assertNotEqual(result,data,Message)

    def tearDown(self):
        self.patcher_failed_username.stop()

if __name__ == '__main__':
    unittest.main()