import random

BET_AMOUNTS = [25, 50, 100, 200, 250, 500]

CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

SUITS = ['♠', '♣', '♥', '♦']


class BlackjackService:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.deck = []
        self.reset_deck()

    def reset_deck(self):
        self.deck = [f"{card}{suit}" for card in CARD_VALUES.keys() for suit in SUITS]
        random.shuffle(self.deck)

    def draw_card(self):
        if len(self.deck) < 10:
            print("Reshuffling deck")
            self.reset_deck()
        return self.deck.pop()

    def calculate_hand(self, hand):
        total = 0
        aces = 0
        for card in hand:
            value = card[:-1]
            total += CARD_VALUES[value]
            if value == 'A':
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def show_hand(self, hand):
        return ' '.join(hand)

    def play_round(self, user):
        print(f"Available bets: {BET_AMOUNTS}")
        try:
            bet = int(input("Enter your bet: "))
            if bet not in BET_AMOUNTS:
                print("Invalid bet amount")
                return
            if bet > user.balance:
                print("Not enough balance")
                return
        except ValueError:
            print("Invalid input!")
            return

        user.adjust_balance(-bet)

        player_hand = [self.draw_card(), self.draw_card()]
        dealer_hand = [self.draw_card(), self.draw_card()]

        print(f"Your hand: {self.show_hand(player_hand)} (Total: {self.calculate_hand(player_hand)})")
        print(f"Dealer shows: {dealer_hand[0]}")

        if self.calculate_hand(player_hand) == 21:
            print("Blackjack! You win 1.5x your bet!")
            user.adjust_balance(int(bet * 2.5))
            return

        while True:
            move = input("Hit or Stand? (h/s): ").lower()
            if move == 'h':
                player_hand.append(self.draw_card())
                print(f"Your hand: {self.show_hand(player_hand)} (Total: {self.calculate_hand(player_hand)})")
                if self.calculate_hand(player_hand) > 21:
                    print(f"You busted with {self.calculate_hand(player_hand)}!")
                    return
            elif move == 's':
                break
            else:
                print("Invalid move.")

        while self.calculate_hand(dealer_hand) < 17:
            dealer_hand.append(self.draw_card())

        player_total = self.calculate_hand(player_hand)
        dealer_total = self.calculate_hand(dealer_hand)

        print(f"Dealer's hand: {self.show_hand(dealer_hand)} (Total: {dealer_total})")

        if dealer_total > 21 or player_total > dealer_total:
            print("You win")
            user.adjust_balance(bet * 2)
        elif player_total == dealer_total:
            print("Draw")
            user.adjust_balance(bet)
        else:
            print("You lose.")
