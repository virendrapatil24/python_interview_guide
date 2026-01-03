import unittest
from unittest.mock import MagicMock
from app import UserManager, Database, divide

class TestMath(unittest.TestCase):
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        
    def test_divide_error(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock(spec=Database)
        self.manager = UserManager(self.mock_db)
        
    def test_get_user_names(self):
        self.mock_db.get_users.return_value = [{"name": "alice"}]
        
        result = self.manager.get_user_names()
        
        self.assertEqual(result, ["ALICE"])
        self.mock_db.get_users.assert_called_once()
        
    def test_add_user(self):
        self.manager.add_user("bob")
        self.mock_db.save_user.assert_called()

if __name__ == '__main__':
    unittest.main()
