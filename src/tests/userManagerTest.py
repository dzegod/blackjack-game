import unittest
from models.userManager import UserManager

class TestCalculator(unittest.TestCase):

    def test_can_create_users_no_users(self):
        can = UserManager().can_create_users()
        self.assertTrue(can)
    def test_can_create_users_max_users(self):
        manager = UserManager()
        manager.users = [{}, {}, {}]
        can = manager.can_create_users()
        self.assertFalse(can)


if __name__ == "__main__":
    unittest.main()
