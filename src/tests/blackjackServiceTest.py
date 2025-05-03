import unittest
from services.blackjackService import BlackjackService
from models.user import User

class TestBlackjackService(unittest.TestCase):
    def setUp(self):
        self.service = BlackjackService(user_manager=None)
        self.service.reset_deck()

    def test_reset_deck_creates_full_52_card_deck(self):
        self.service.deck = []
        self.service.reset_deck()
        self.assertEqual(len(self.service.deck), 52)
        self.assertEqual(len(set(self.service.deck)), 52)

    def test_draw_card_reduces_deck_size(self):
        before = len(self.service.deck)
        card = self.service.draw_card()
        self.assertIsInstance(card, str)
        self.assertEqual(len(self.service.deck), before - 1)

    def test_draw_card_triggers_reshuffle_when_deck_small(self):
        self.service.deck = ['X'] * 5
        card = self.service.draw_card()
        self.assertEqual(len(self.service.deck), 51)
        self.assertIsInstance(card, str)

    def test_calculate_hand_without_aces(self):
        hand = ['2♠', '10♥', 'K♦']
        self.assertEqual(self.service.calculate_hand(hand), 2 + 10 + 10)

    def test_calculate_hand_single_ace(self):
        hand = ['A♠', '9♥']
        self.assertEqual(self.service.calculate_hand(hand), 20)

    def test_calculate_hand_multiple_aces_adjusted(self):
        hand = ['A♠', 'A♥', '9♦', 'K♣']
        self.assertEqual(self.service.calculate_hand(hand), 21)

    def test_get_card_value(self):
        self.assertEqual(self.service.get_card_value('10♣'), 10)
        self.assertEqual(self.service.get_card_value('J♦'), 10)
        self.assertEqual(self.service.get_card_value('A♥'), 11)
        self.assertEqual(self.service.get_card_value('Z?'), 0)

    def test_show_hand(self):
        hand = ['2♠', 'J♦']
        self.assertEqual(self.service.show_hand(hand), '2♠ J♦')

    def _make_deck(self, suffix_cards):
        prefix_len = 52 - len(suffix_cards)
        prefix = ['2♠'] * prefix_len
        return prefix + list(suffix_cards)

    def test_play_round_gui_player_blackjack_wins(self):
        user = User('T', balance=1000)
        svc = BlackjackService(None)
        svc.deck = self._make_deck(['J♦', 'Q♣', 'K♥', 'A♠'])
        result = svc.play_round_gui(user, bet=100)
        self.assertIn("Blackjack! You win!", result)
        self.assertEqual(user.balance, 1150)

    def test_play_round_gui_both_blackjack_draw(self):
        user = User('T', balance=1000)
        svc = BlackjackService(None)
        svc.deck = self._make_deck(['K♥', 'A♠', 'K♦', 'A♣'])
        result = svc.play_round_gui(user, bet=100)
        self.assertIn("Both have blackjack! It's a draw.", result)
        self.assertEqual(user.balance, 1000)

    def test_play_round_gui_player_busts(self):
        user = User('T', balance=500)
        svc = BlackjackService(user_manager=None)
        svc.deck = self._make_deck(['X','9♦','3♣','2♥','9♥','5♣'])
        result = svc.play_round_gui(user, bet=100)
        self.assertIn("You busted! Final hand:", result)
        self.assertEqual(user.balance, 400)

if __name__ == "__main__":
    unittest.main(verbosity=2)
