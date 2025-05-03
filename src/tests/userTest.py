import unittest
from models.user import User

class TestCalculator(unittest.TestCase):

    def test_user_add_money(self):
        user = User('Donatas', 500)
        user.adjust_balance(500)
        self.assertEqual(user.balance, 1000)
    def test_user_subtract_money(self):
        user = User('Donatas', 500)
        user.adjust_balance(-1000)
        self.assertEqual(user.balance, 0)
    def test_balance_never_negative(self):
        user = User("Donatas", 500)
        user.adjust_balance(-200)
        self.assertEqual(user.balance, 300)
    def test_to_dict(self):
        user = User("Donatas", 420)
        expected = {"nickname": "Donatas", "balance": 420}
        self.assertDictEqual(user.to_dict(), expected)

if __name__ == "__main__":
    unittest.main()
