import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from models.userManager import UserManager
from services.blackjackService import BlackjackService

BET_AMOUNTS = [25, 50, 100, 200, 250, 500]


class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")
        self.root.geometry("1280x720")
        self.root.configure(bg="#0B6623")

        self.manager = UserManager()
        self.game = BlackjackService(self.manager)
        self.user = None
        self.fullscreen = False

        self.login_frame = self._create_login_frame()
        self.game_frame = self._create_game_frame()
        self.login_frame.pack(fill="both", expand=True)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def close_game(self):
        self.root.quit()

    def _create_login_frame(self):
        frame = tk.Frame(self.root, bg="#0B6623")

        tk.Label(
            frame, text="Welcome to Blackjack!",
            font=("Arial", 24), bg="#0B6623", fg="white"
        ).pack(pady=30)

        tk.Label(
            frame, text="Enter nickname:",
            font=("Arial", 16), bg="#0B6623", fg="white"
        ).pack()

        self.nickname_entry = tk.Entry(
            frame, font=("Arial", 16), width=20
        )
        self.nickname_entry.pack(pady=15)

        tk.Button(
            frame, text="Login",
            font=("Arial", 16), bg="gold", width=10,
            command=self.login_user
        ).pack(pady=10)

        tk.Button(
            frame, text="Register",
            font=("Arial", 16), bg="lightblue", width=10,
            command=self.register_user
        ).pack(pady=10)

        tk.Button(
            frame, text="Fullscreen Mode",
            font=("Arial", 14), bg="gray", fg="white",
            command=self.toggle_fullscreen
        ).pack(pady=5)

        tk.Button(
            frame, text="Close Game",
            font=("Arial", 14), bg="darkred", fg="white",
            command=self.close_game
        ).pack(pady=5)

        return frame

    def _create_game_frame(self):
        frame = tk.Frame(self.root, bg="#0B6623")

        self.status_label = tk.Label(
            frame, text="", font=("Arial", 20, "bold"),
            bg="#0B6623", fg="white"
        )
        self.status_label.pack(pady=20)

        self.balance_label = tk.Label(
            frame, text="Balance: 0",
            font=("Arial", 18), bg="#0B6623", fg="white"
        )
        self.balance_label.pack(anchor="ne", padx=20)

        bet_box = tk.Frame(frame, bg="#0B6623")
        bet_box.pack(pady=10)
        tk.Label(
            bet_box, text="Bet amount:",
            font=("Arial", 16), bg="#0B6623", fg="white"
        ).pack(side="left", padx=(0, 10))
        self.bet_var = tk.IntVar(value=BET_AMOUNTS[0])
        bet_menu = tk.OptionMenu(bet_box, self.bet_var, *BET_AMOUNTS)
        bet_menu.config(font=("Arial", 16))
        bet_menu["menu"].config(font=("Arial", 16))
        bet_menu.pack(side="left")

        self.play_button = tk.Button(
            frame, text="New Round",
            font=("Arial", 18), bg="gold", width=12,
            command=self.play_round
        )
        self.play_button.pack(pady=15)

        tk.Label(
            frame, text="Dealer's Hand",
            font=("Arial", 18), bg="#0B6623", fg="white"
        ).pack(pady=(20, 5))
        self.dealer_card_frame = tk.Frame(frame, bg="#0B6623")
        self.dealer_card_frame.pack()
        self.dealer_value_label = tk.Label(
            frame, text="Value: ?",
            font=("Arial", 16), bg="#0B6623", fg="white"
        )
        self.dealer_value_label.pack(pady=5)

        tk.Label(
            frame, text="Your Hand",
            font=("Arial", 18), bg="#0B6623", fg="white"
        ).pack(pady=(30, 5))
        self.card_frame = tk.Frame(frame, bg="#0B6623")
        self.card_frame.pack()
        self.player_value_label = tk.Label(
            frame, text="Value: 0",
            font=("Arial", 16), bg="#0B6623", fg="white"
        )
        self.player_value_label.pack(pady=5)

        self.button_frame = tk.Frame(frame, bg="#0B6623")
        self.button_frame.pack(pady=20)

        self.output_text = tk.Label(
            frame, text="", font=("Arial", 16),
            wraplength=800, justify="center",
            bg="#0B6623", fg="white"
        )
        self.output_text.pack(pady=10)

        tk.Button(
            frame, text="Fullscreen Mode",
            font=("Arial", 14), bg="gray", fg="white",
            command=self.toggle_fullscreen
        ).pack(pady=3)

        tk.Button(
            frame, text="Close Game",
            font=("Arial", 14), bg="darkred", fg="white",
            command=self.close_game
        ).pack(pady=3)

        tk.Button(
            frame, text="Logout",
            font=("Arial", 18), bg="red", fg="white", width=12,
            command=self.logout
        ).pack(pady=3)

        return frame

    def load_card_image(self, card_code):
        rank = card_code[:-1]
        suit_char = card_code[-1]
        suit_map = {
            '♠': 'spades', '♥': 'hearts',
            '♦': 'diamonds', '♣': 'clubs'
        }
        suit = suit_map[suit_char]
        path = os.path.join("cards", f"{suit}_{rank}.png")
        img = Image.open(path).resize((120, 180))
        return ImageTk.PhotoImage(img)

    def clear_card_frames(self):
        for frame in (self.dealer_card_frame, self.card_frame, self.button_frame):
            for w in frame.winfo_children():
                w.destroy()
        self.status_label.config(text="")
        self.dealer_value_label.config(text="Value: ?")
        self.player_value_label.config(text="Value: 0")
        self.output_text.config(text="")

    def play_round(self):
        self.play_button.config(state="disabled")
        self.clear_card_frames()
        bet = self.bet_var.get()

        try:
            if bet not in BET_AMOUNTS:
                raise ValueError("Select bet from dropdown.")
            if bet > self.user.balance:
                raise ValueError("Not enough balance.")

            self.player_cards = [self.game.draw_card(), self.game.draw_card()]
            self.dealer_cards = [self.game.draw_card(), self.game.draw_card()]
            self.bet_amount = bet

            for c in self.player_cards:
                self._add_card_to_frame(c, self.card_frame)
            self._add_card_to_frame(self.dealer_cards[0], self.dealer_card_frame)

            self.user.adjust_balance(-bet)
            self.manager.save_users()
            self.update_balance()

            self.status_label.config(text="Your Turn")
            self._update_values(show_dealer=False)

            self.hit_button = tk.Button(
                self.button_frame, text="Hit",
                font=("Arial", 16), bg="white", width=8,
                command=self.hit_card
            )
            self.stand_button = tk.Button(
                self.button_frame, text="Stand",
                font=("Arial", 16), bg="white", width=8,
                command=self.stand
            )
            self.hit_button.pack(side="left", padx=30)
            self.stand_button.pack(side="left", padx=30)

        except Exception as e:
            self.play_button.config(state="normal")
            messagebox.showerror("Error", str(e))

    def hit_card(self):
        card = self.game.draw_card()
        self.player_cards.append(card)
        self._add_card_to_frame(card, self.card_frame)
        self._update_values(show_dealer=False)
        if self.game.calculate_hand(self.player_cards) > 21:
            self.status_label.config(text="You busted")
            self.end_round(player_busted=True)

    def stand(self):
        self.status_label.config(text="Dealer's Turn")
        self._reveal_dealer_cards()
        self._update_values(show_dealer=True)
        while self.game.calculate_hand(self.dealer_cards) < 17:
            c = self.game.draw_card()
            self.dealer_cards.append(c)
            self._add_card_to_frame(c, self.dealer_card_frame)
            self._update_values(show_dealer=True)
        self.end_round()

    def end_round(self, player_busted=False):
        p_total = self.game.calculate_hand(self.player_cards)
        d_total = self.game.calculate_hand(self.dealer_cards)

        if player_busted:
            res = f"You busted with {p_total}. You lose."
        else:
            if d_total > 21 or p_total > d_total:
                res = f"You win! ({p_total} vs {d_total})"
                self.user.adjust_balance(self.bet_amount * 2)
            elif d_total == p_total:
                res = f"Draw. ({p_total} vs {d_total})"
                self.user.adjust_balance(self.bet_amount)
            else:
                res = f"You lose. ({p_total} vs {d_total})"

        self.manager.save_users()
        self.output_text.config(text=res)
        self.status_label.config(text="Round Finished")
        self._update_values(show_dealer=True)
        self.update_balance()
        self.disable_action_buttons()
        self.play_button.config(state="normal")

        if self.user.balance <= 0:
            messagebox.showinfo(
                "Account Closed",
                "Your balance is zero. Account has been removed."
            )
            del self.manager.users[self.user.nickname]
            self.manager.save_users()
            self.logout()

    def _add_card_to_frame(self, card_code, frame):
        img = self.load_card_image(card_code)
        lbl = tk.Label(frame, image=img, bg="#0B6623")
        lbl.image = img
        lbl.pack(side="left", padx=10)

    def _reveal_dealer_cards(self):
        for w in self.dealer_card_frame.winfo_children():
            w.destroy()
        for c in self.dealer_cards:
            self._add_card_to_frame(c, self.dealer_card_frame)

    def disable_action_buttons(self):
        for w in self.button_frame.winfo_children():
            w.destroy()

    def _update_values(self, show_dealer):
        if show_dealer:
            dealer_value = self.game.calculate_hand(self.dealer_cards)
        else:
            dealer_value = self.game.get_card_value(self.dealer_cards[0])
        self.dealer_value_label.config(text=f"Value: {dealer_value}")
        self.player_value_label.config(
            text=f"Value: {self.game.calculate_hand(self.player_cards)}"
        )

    def update_balance(self):
        bal = self.user.balance
        self.balance_label.config(text=f"Balance: {bal}")

    def login_user(self):
        nick = self.nickname_entry.get().strip()
        if not nick:
            messagebox.showwarning("Warning", "Please enter a nickname.")
            return

        user = self.manager.get_user(nick)
        if user:
            if user.balance <= 0:
                messagebox.showinfo(
                    "Account Closed",
                    "Your balance is zero. Account has been removed."
                )
                del self.manager.users[nick]
                self.manager.save_users()
                self.nickname_entry.delete(0, tk.END)
                return
            self.user = user
            self.show_game_frame()
        else:
            messagebox.showerror("Error", "Incorrect nickname.")
            self.nickname_entry.delete(0, tk.END)

    def register_user(self):
        nick = self.nickname_entry.get().strip()
        if not nick:
            messagebox.showwarning("Warning", "Please enter a nickname.")
            return

        if self.manager.get_user(nick):
            messagebox.showerror("Error", "Nickname already taken.")
            return

        if not self.manager.can_create_users():
            messagebox.showerror(
                "Error",
                f"Maximum of {self.manager.MAX_USERS} users reached."
            )
            return

        self.user = self.manager.register_user(nick)
        self.manager.save_users()
        self.show_game_frame()

    def show_game_frame(self):
        self.login_frame.pack_forget()
        self.status_label.config(text="Ready to play")
        self.output_text.config(text="")
        self.update_balance()
        self.game_frame.pack(fill="both", expand=True)

    def logout(self):
        self.game_frame.pack_forget()
        self.nickname_entry.delete(0, tk.END)
        self.login_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
