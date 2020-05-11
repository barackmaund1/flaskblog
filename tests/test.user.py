import unittest
from app.models import User,Post

class UserTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username = 'test',email='test12@gmail.com',bio='default bio',password='albert')

    def test_password_setter(self):
        self.assertTrue(self.new_user.hashed_password is not None)

    def test_no_password_access(self):
        with self.assertTrue(AttributeError):
            self.new_user.hashed_password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('albert'))