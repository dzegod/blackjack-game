# blackjack-game

---

## Introduction

**WHAT IS IT**

Blackjack is a globally popular card game—easy to learn, addictive to play. Casinos love it because it keeps players coming back for more. In this program, **Blackjack-game**, you face the same odds, but with one difference: every round shuffles a fresh deck, so no card counting—just pure luck and fun.

---

## Main Menu

When you start the program there will be a few options, controlled by numbers:

1. **Continue** – it saves your progress (nickname, coins);  
2. **Register** – if you are a new member. You will be asked for your nickname and start with 500 coins;  
3. **Close** – closes the program.

Maximum users you can have is 3. When you reach the limit, the program will say “Maximum number of users reached.”

---

## Game Play

1. **Place Your Bet** – Choose from preset amounts: 25, 50, 100, 200, 250, or 500 coins.  
2. **Your Hand** – You start with two cards. Your total is displayed.  
3. **Hit or Stand** –  
   - **Hit**: Draw another card.  
   - **Stand**: End your turn; dealer plays automatically.  
4. **Dealer’s Turn** – Dealer draws until reaching at least 17.  
5. **Outcome** –  
   - **Blackjack** (21 on first two cards): pays 1.5× your bet.  
   - **Win**: your total > dealer’s or dealer busts: you earn 2× your bet.  
   - **Draw**: totals tie: you get your bet back.  
   - **Lose**: dealer’s total > yours: you lose your bet.  

---

## Testing

All core functionality is covered by unit tests using Python’s built-in `unittest` framework. Tests live in the `src/tests/` directory and verify deck behavior, hand evaluation logic, and game service methods.

---

## Code Style

The code adheres to PEP8 style conventions. Naming follows `snake_case` for functions and variables, `PascalCase` for classes, and lines are wrapped at 79 characters. You can use tools like `flake8` to enforce style rules.

---

Enjoy testing your luck and strategy—no real money, no counting, just a good time!
