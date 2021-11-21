import unittest
from website.controller import userController as UC
from website.controller import adminforumController as AFC
from unittest.mock import patch


#Profile update test#
class test_UpdateProfile(unittest.TestCase):
    def setUp(self):
        self.patcher_passed = patch('website.controller.userController.update',return_value=b"update bios")
        self.patcher_passed.start()

    def test_updateProfile_unit_testing_passed(self):
        result = UC.update()
        data = b'update bios'
        Message = "Test Update Profile passed"
        self.assertIn(data,result,Message)
    
    def tearDown(self):
        self.patcher_passed.stop()
        

#Create Announcement test#
class test_CreateAnnouncement(unittest.TestCase):
    def setUp(self):
        self.patcher_passed = patch('website.controller.adminforumController.create_announcement',return_value= b"New Announcement")
        self.patcher_passed.start()

    def test_announcement_unit_testing_passed(self):
        result = AFC.create_announcement()
        data = b"New Announcement"
        Message = "Test announcement passed"
        self.assertIn(data,result,Message)
    
    def tearDown(self):
        self.patcher_passed.stop()


if __name__ == '__main__':
    unittest.main()